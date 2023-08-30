---
layout: post
title: "[Python] kafka-python을 통한 실시간 kudu cdc" #게시물 이름
tags: [pyhton, Kafka, kudu, consumer, 카프카, CDC] #태그 설정
categories: python #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

<https://byj1009.github.io/python/2023/07/19/python-kafka.html> 에서 만든 CDC 예제 데이터를 활용한 kudu table 실시간(?) CDC를 구현했던 코드를 정리해본다.   
Cloudera Data Platform을 활용해서 빅데이터 플랫폼이 구축이 되어 있으며, python3.6.4 버전을 사용했기 때문에 제약이 많았다.

Python3.x에서는 Python에서 바로 Kudu로 접근이 불가능하므로, Apache Impala를 통한 CDC를 구현했다.(초당 20건 정도, 성능이 너무 느리다...)
나중에 기회가 된다면, python2.x 버전에서 지원하는 kudu-python 패키지를 활용해서 테스트 해봐야겠다...   


# 0. 버전정보
## 0.1 테스트 환경
- Linux, Rhel8.6
- Python3.6.4 (Rhel8.6 default python)
- kerberos enabled

# 1. 사전 설정 작업
## 1.1 Python venv 설정

Linux 환경에서 Python 가상환경을 구성한다.
``` bash
#python3 -m venv [Path]
python3 -m venv /python/python_kafka

# activate
# cd [Path]/bin
cd /python/python_kafka/bin
source activate
```

## 1.2 Python Package 설치

``` bash
pip install --upgrade pip
pip install -r requirements.txt
```

깨알 정보로, 현재 실행중인 python인터프리터의 pip list 항목을 requirements.txt로 만들 수 있다.
`$pip freeze > requirements.txt` 

``` txt
$cat requirements.txt
absl-py==0.15.0
astunparse==1.6.3
attrs==22.2.0
bitarray==2.7.5
cached-property==1.5.2
cachetools==4.2.4
certifi==2023.5.7
charset-normalizer==2.0.12
clang==5.0
dataclasses==0.8
decorator==5.1.1
fasteners==0.15
flatbuffers==1.12
fsspec==2022.1.0
gast==0.4.0
google-auth==1.35.0
google-auth-oauthlib==0.4.6
google-pasta==0.2.0
grpcio==1.48.2
gssapi==1.7.3
h5py==3.1.0
idna==3.4
importlib-metadata==4.8.3
impyla==0.18.0
iniconfig==1.1.1
kafka-python==2.0.2
keras==2.6.0
Keras-Preprocessing==1.1.2
kerberos==1.3.1
krbcontext==0.10
krbticket==1.0.6
Markdown==3.3.7
monotonic==1.6
mypy==0.921
mypy-extensions==0.4.4
numpy==1.19.5
oauthlib==3.2.2
opt-einsum==3.3.0
packaging==21.3
pandas==1.1.5
pluggy==1.0.0
polars==0.12.5
protobuf==3.19.6
psutil==5.9.5
pure-sasl==0.6.2
py==1.11.0
pyarrow==6.0.1
pyasn1==0.5.0
pyasn1-modules==0.3.0
pybind11==2.10.4
pyparsing==3.1.0
pytest==7.0.1
python-dateutil==2.8.2
pytz==2023.3
requests==2.27.1
requests-oauthlib==1.3.1
retrying==1.3.3
rsa==4.9
setuptools-scm==6.4.2
six==1.15.0
tensorboard==2.6.0
tensorboard-data-server==0.6.1
tensorboard-plugin-wit==1.8.1
tensorflow==2.6.2
tensorflow-estimator==2.6.0
termcolor==1.1.0
thrift==0.16.0
thrift-sasl==0.4.3
tomli==1.2.3
typed-ast==1.5.4
typing-extensions==3.7.4.3
urllib3==1.26.16
Werkzeug==2.0.3
wrapt==1.12.1
zipp==3.6.0
```

# 2. Python kafka to kudu file 작성

CDC 테스트에 Json형식의 예제 데이터는 아래와 같다.

data = {"before":{
                "id": 1,
                "val": 123
                },
        "after":{
            "id": 1,
            "val": 321
                }
        }


### 2.1 cdc_test.py 파일

for문으로 json 형식의 데이터를 한줄씩 읽어 Impala를 통한 Query를 날리는데... Insert, Update, Delete 한 쿼리당 약 80ms정도 소요가 되며,   
테스트데이터 12,000건에 대해서 11분 정도가 소요가 된 것으로 보아... 초당 10건을 처리하는 것 같다. 한마디로 쓰레기.


``` python
from impala.dbapi import connect
from kafka import KafkaConsumer
from krbcontext.context import krbContext
import json

### 0. variable 작성
bootstrap_server=['bootstrap_server_IP:9092']
topic_name="cdctopic"
consumer_group_name="cdc_test_group"
table_name="testdb.cdc_table"

### 1. Kerberos 인증을 위한 krbContext 구문 작성
with krbContext(using_keytab=True, principal='test@REALM.COM', keytab_file='/etc/security/keytabs/test.keytab', ccache_file='/tmp/krb5cc_pid_kafka_test'):
    conn = connect(
        host = "impala_daemon_server_INFO", 
        port = 21050, 
        auth_mechanism='GSSAPI',
        kerberos_service_name = "impala")
    cursor = conn.cursor()

### 2. Data Parsing
# UPDATE QUERY USING IMPALA
def execute_update_query(cursor, tablename, parsed_data):
    for key, value in parsed_data["after"].items():
        if key=="id":
            primary_key_val=value
        elif key=="val":
            update_val=value
    cursor.execute("UPDATE %s SET val=%d WHERE id=%d" % (table_name, update_val, primary_key_val))

# DELETE QUERY USING IMPALA
def execute_delete_query(cursor, tablename, parsed_data):
    for key, value in parsed_data["before"].items():
        if key=="id":
            primary_key_val=value
    cursor.execute("DELETE FROM %s WHERE id=%d" % (table_name, primary_key_val))

# INSERT QUERY USING IMPALA
def execute_update_query(cursor, tablename, parsed_data):
    for key, value in parsed_data["after"].items():
        if key=="id":
            primary_key_val=value
        elif key=="val":
            update_val=value
    cursor.execute("INSERT INTO %s VALUES (%d, %d)" % (table_name, primary_key_val, update_val))

### 3. KafkaConsumer
    try:
        consumer = KafkaConsumer(topic_name,
                                group_id=consumer_group_name,
                                bootstrap_servers=bootstrap_server,
                                enable_auto_commit=True,
                                auto_offset_reset='latest', # earliest, latest, none
                                sasl_mechanism='GSSAPI',
                                security_protocol='SASL_PLAINTEXT',
                                sasl_kerberos_service_name='kafka'
                                )
        ### 2.1 Read Topic record (cdc transaction log)
        for message in consumer:
            parsed_data = json.loads(message.value) # Load topic messages in JSON format.
            
            # Initialization
            primary_key_val=0
            update_val=0
            
            if "before" in parsed_data and "after" in parsed_data:
                execute_update_query(cursor, tablename, parsed_data)
            
            elif "before" in parsed_data and "after" not in parsed_data: # DELETE
                execute_update_query(cursor, tablename, parsed_data)
            
            elif "before" not in parsed_data and "after" in parsed_data: #INSERT
                execute_update_query(cursor, tablename, parsed_data)
                
    except Exception as e:
        print("An error occurred:", str(e))
    
    cursor.close()
    conn.close()
```






impala를 통해서 처리를 하다보니 너무 느린 것 같다. 배치성으로 작업을 한다면 효율이 좋겠지만... 테스트의 가치를 느끼지 못해 Spark Structured Streaming으로 테스트를 이어 진행 중






---
### Reference

[needjarvis 티스토리 블로그][tstory]
[kafka-pythony document][kafka-python]

[tstory]: https://needjarvis.tistory.com/607
[kafka-python]: https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html