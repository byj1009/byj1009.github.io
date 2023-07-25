---
layout: post
title: "[Python] Python으로 Kafka Producer 구현" #게시물 이름
tags: [pyhton, Kafka, Topic, Producer, producing, 카프카] #태그 설정
categories: python #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

프로젝트 준비로 Change Data Capture를 테스트하다 보니, 테스트 데이터셋을 Kafka에 Producing해야했고, Python에 있는 python-kafka 패키지를 통해 간단하게 구현 할 수 있었다.   

# 0. 버전정보
## 0.1 테스트 환경

- Linux, Rhel8.6
- Python3.6.4 (Rhel8.6 default python)
- kerberos enabled

## 0.2 Python Package 정보
``` txt
$pip list
decorator    5.1.1
gssapi       1.7.3
kafka-python 2.0.2
krbcontext   0.10
pip          21.3.1
setuptools   39.2.0
```

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

krbcontext는 kerberized된 Kafka 연결에 필요한 패키지   
``` bash
pip install --upgrade pip
pip install kafka-python krbcontext
```

# 2. Python kafka Producer file 작성

CDC 테스트에 Json형식의 예제 데이터는 아래와 같다.

```
date = {"before":{
                "id": 1,
                "val": 123
                },
        "after":{
            "id": 1,
            "val": 321
                }
        }
```

### 2.1 예제 코드

``` python
from kafka import KafkaProducer
from krbcontext.context import krbContext
import time

with krbContext(using_keytab=True, principal='test@EXAMPLE.COM', keytab_file='/etc/security/keytabs/test.keytab', ccache_file='/tmp/krb5cc_example'):
    try:
        producer = KafkaProducer(bootstrap_servers=['bootstrap_server_IP:9092'],
                                 acks=1,
                                 sasl_mechanism='GSSAPI',
                                 security_protocol='SASL_PLAINTEXT',
                                 sasl_kerberos_service_name='kafka',
                                 value_serializer=lambda x: json.dumps(x).encode('utf-8')
                                 )
        start = time.time() # Producing 시작시간
        
        for i in range(10000):
            data = {'id': i,'val': i} # { Key : value, json 형식의 데이터 스키마}
            producer.send('test_topic', value=data) # test_topic에 data라는 value를 produsing
            producer.flush() #건 바이 건으로 배치 처리하지 않고, 보류 중인 모든 메시지 즉시 전송
        print("Total time : ", time.time() - start)
```


### 2.2 실제 테스트 코드

Chagne Data Capture(CDC)를 테스트 하기 위해서 Insert, Update, Delete에 대한 테스트데이터를 Producing하기 위한 코드이다.   
- Before : Null, After 존재 > Insert
- Before : 존재, Before Null > Delete
- Before : 존재, AFter 존재 > Update


``` python
#! /usr/bin/python3
from kafka import KafkaProducer
from krbcontext.context import krbContext
import time
import json

### krbContext를 with문으로 사용해 프로세스가 떠 있는 동안 Keytab파일을 이용한 Kerberos인증을 하도록 작성.
### keytab_file의 저장 위치와, ccache_file의 위치는 사용자 지정
with krbContext(using_keytab=True, principal='test@REALM_INFO', keytab_file='/etc/security/keytabs/test.keytab', ccache_file='/tmp/krb5cc_pid_kafka_prod'):
    try:
        producer = KafkaProducer(bootstrap_servers=['kafka_server:9092'],
                                 acks=1,
                                 sasl_mechanism='GSSAPI',
                                 security_protocol='SASL_PLAINTEXT',
                                 sasl_kerberos_service_name='kafka',
                                 value_serializer=lambda x: json.dumps(x).encode('utf-8')
                                 )
        
        for i in range(1,1001):
            data = {"after":{"id": i,"val": 100}} #insert
            producer.send('cdctopic',value=data) # 메세지 전송
            producer.flush() #배치 처리하지 않고, 보류 중인 모든 메시지 즉시 전송

        for i in range(10,1001):
            data = {"before":{"id": i,"val": 200},"after":{"id": i,"val": 724}} #update
            producer.send('cdctopic',value=data) # 메세지 전송
            producer.flush() #배치 처리하지 않고, 보류 중인 모든 메시지 즉시 전송

        for i in range(50,1001):
            data = {"before":{"id": i,"val": 200}} #delete
            producer.send('cdctopic',value=data) # 메세지 전송
            producer.flush() #배치 처리하지 않고, 보류 중인 모든 메시지 즉시 전송

        
    except Exception as e:
        print("An error occurred:", str(e))
    pass

```

# 3. Kafka Topic 생성 (참고용)

Kerberos가 적용된 Kafka Broker에 Topic을 생성하기 위한 작업이다.

## 3.1 jaas.conf, client.properties 작성

JAAS(Java Authentication and Authorization Service), JAAS(Java Authentication and Authorization Service)는 자바 프로그래밍 언어의 보안 프레임워크이다.   
jaas.conf에 Kerberized Kafka Broker에 Connect 하기 위해 필요한 Client 정보를 작성하는 것.

client.propperties 내용도 `kafka-topics --option` 과 같이 옵션으로 명시가 가능하나, 파일로 명령어 config를 관리하기 위해 작성한다.


### 3.1.1 jaas.conf

/etc/security/keytabs/ 아래 경로로 관련 keytab파일을 copy해서 사용하면 된다.

``` txt
KafkaClient {
 com.sun.security.auth.module.Krb5LoginModule required
 useKeyTab=true
 keyTab="/etc/security/keytabs/kafka.keytab"
 storeKey=true
 useTicketCache=false
 principal="kafka@REALM.COM";
};
Client {
  com.sun.security.auth.module.Krb5LoginModule required
  useKeyTab=true
  storeKey=true
  useTicketCache=false
  keyTab="/etc/security/keytabs/kafka.keytab"
  principal="kafka@REALM.COM";
};
```

### 3.1.2 client.properties
``` txt
security.protocol=SASL_PLAINTEXT
sasl.kerberos.service.name=kafka
```

## 3.2 Kafka Topic 생성

작업 Linux 터미널(Session)에서 커버로스 관련 인증을 위해 아래의 명령어를 실행한다.
추가적으로, CDC의 경우 데이터의 순차성보장이 매우매우 중요하기 때문에 partition의 수는 1로 고정이다... Kafka의 동작원리를 공부해보면 이해가 가능할 것.

``` bash
# 필자는 권한관리를 위한 Ranger가 세팅되어 있기 때문에 Kafka topic create 권한을 가진 유저의 keytab을 활용했다.
kinit -kw kafka.keytab kafka@REALM

export KAFKA_OPTS="-Djava.security.auth.login.config=/etc/security/keytabs/jaas.conf"

# topic list 조회
kafka-topics --list --bootstrap-server=cfm01.goodmit.com:9092 --command-config client.properties

kafka-topics --create --topic test_topic --partitions 1 --bootstrap-server=cfm01.goodmit.com:9092 --command-config client.properties

```


---
### Reference
[needjarvis 티스토리 블로그][tstory]


[tstory]: https://needjarvis.tistory.com/607