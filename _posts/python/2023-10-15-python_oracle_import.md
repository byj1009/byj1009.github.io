---
layout: post
title: "[Python] cx_Oracle을 이용한 Oracle table 저장하기" #게시물 이름
tags: [python, oracle, cx_oracle, parquet, hive, hdfs] #태그 설정
categories: python #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

Python을 통해 Oracle 테이블을 핸들링하기 위한 Python Package로 cx_Oracle을 사용이 가능하다.
본인은, oracle table을 Apache Kudu에 이관하기 위해서 cx_Oracle을 사용했다.

# Prerequisites
cx_Oracle 8.3 has been tested with Python versions 3.6 through 3.10. You can use cx_Oracle with Oracle 11.2, 12c, 18c, 19c and 21c client libraries.
<https://pypi.org/project/cx-Oracle/>

파이썬은 python3.6.8 버전에서 테스트 사용했고, Oracle은 11g 환경에서 테스트를 진행했다.

# cx_Oracle



## 1. 환경세팅
| Name | Version |
| --- | --- |
| Linux | Rhel8.6 |
| Postgresql | 14.8-2 |
| Python | 3.9.7 |
| Apache Airflow | 2.7.0 |


### Python Install

Apache Airflow를 사용하기 위해서는 Python3.8 이상 버전이 필요하다. Rhel8.6 OS image에 내장되어 있는 Python3.9.7 버전을 이용할 것이다.

``` bash
yum install python3.9

# 다른 Python 버전을 사용하고 있다면 편의성을 위해 Default Python version을 변경하자.
update-alternatives --config python
```


### Pip install Airflow

pip통해서 apache-airflow 설치를 위해 버전을 업그레이드 한다.   
또한, 공식사이트에 나와 있는 설치 가이드에 따라 진행을 하다 보면 TLS/SSL 인증서 관련한 에러가 발생할 수 있다.   
이러한 문제를 해결하기 위해 --trusted-host 옵션으로 관련 Site SSL인증을 Pass할 수 있도록 설정해주었다.

```bash

pip3 install --upgrade pip

pip3 install 'apache-airflow==2.7.0'  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.7.0/constraints-3.9.txt" --trusted-host raw.githubusercontent.com --trusted-host pypi.org

```

관련 SSL 에러   
```python
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain (_ssl.c:1129)'))'
```

### psycopg2, postgresql-client 설치

Apache Airflow가 설치되는 서버와 Postgresql(Metadata Database)의 연결을 위해서 관련 postgresql, python psycopg2 라이브러리를 설치한다.

``` bash
# Rhel8.6에 내장되어 있는 postgresql10 버전을 사용하지 않기 위해 아래의 명령어 실행 후, 별도의 Postgresql14 Repository를 잡아 설치할 것.
dnf -qy module disable postgresql
yum install postgresql14 python39-devel.x86_64
yum install perl clang-devel libicu-devel llvm-devel 
```

### database setting ( postgresql14 )
postgresql Database를 설치하면, 초기 initdb, pg_hba.conf 수정과 같은 작업이 필요하다.
본 글에서는 관련 내용은 다루지 않는다.

```sql
sudo -u postgres psql

CREATE DATABASE airflow_db;
CREATE USER airflow_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;

```

++ 추가적으로 Postgresql 15버전 이상에서는 아래의 별도 명령어가 필요하다. 물론 Postgresql14에서는 불필요.

```SQL
-- airflow_db 데이터베이스에 연결
\c airflow_db;
-- public 스키마에 대한 모든 권한을 airflow_user에게 부여
GRANT ALL PRIVILEGES ON SCHEMA public TO airflow_user;
```


## Airflow 설정
### RDB정보 확인
Airflow 첫 설치시 기본으로 설정되어 있는 RDB정보를 조회할 수 있다. Default 설정으로 sqlite를 바라 보도록 설정이 되어있으나, 앞서 위에 작성한 내용과 같이 sqlite는 테스트 용으로만 쓰라는데... ~~~운영에 적합하다는 postgresql을 기본으로 설정해 주는게 맞지 않나?~~~

```
airflow config get-value database sql_alchemy_conn
>> sqlite:////tmp/airflow/airflow.db
```
### Database 정보 입력
Airflow가 Postgresql Database에 액세스 할 수 있도록 RDB정보를 수정해주어야 한다.

```bash
vi /root/airflow/airflow.cfg

#sql_alchemy_conn = sqlite:////root/airflow/airflow.db
sql_alchemy_conn = postgresql+psycopg2://{ID}:{PW}@{서버 FQDN}/{airflow db name}
#예시
sql_alchemy_conn = postgresql+psycopg2://airflow_user:password@test.server.com/airflow_db
```

### psycopg2 파이썬 라이브러리 설치
postgresql에 연결하기 위한 파이썬 라이브러리를 설치해야 한다. pypi에서 필요한 rpm파일을 받을 수 있다.
<https://pypi.org/project/psycopg2/>

```
pip install wheel
rpm -ivh python39-psycopg2-2.9.6-1.rhel8.x86_64.rpm
```
### migrate
airflow db migrate


airflow users create \
	--username admin \
	--firstname byun \
	--lastname tester \
	--role Admin \
	--email byj920501@gmail.com
	
# 임시방편 데몬 프로세스 실행 >>> 나중에 systemd 데몬 등록해야함
airflow webserver --port 8080 > /root/airflow/logs/stdin.log 2> /root/airflow/logs/stdout.log &








---
### Reference

[needjarvis 티스토리 블로그][tstory]
[kafka-pythony document][kafka-python]

[tstory]: https://needjarvis.tistory.com/607
[kafka-python]: https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html



















#!/usr/bin/env python
# coding: utf-8
import os
import cx_Oracle
import pandas as pd
org_query = """
SELECT ROWID, {0}
FROM {1}
ORDER BY ROWID
WHERE ROWNUM < {3} AND ROWNUM >= {2}
"""

#####################################
## 수정 또는 인자로 넘어와야 할곳
#####################################
table_schema = """
              ID,
              ST1,
              ST2,
              NUM1
"""
#####################################
## 수정 또는 인자로 넘어와야 할곳
#####################################
table_name = "TESTER.TEST_CLOB_TABLE"

start_num = 1
page_size = 20 # batch size
connect = cx_Oracle.connect("id", "password", "10.200.xxx.xxx:1521/SID")
cur = connect.cursor()

# 테이블의 데이터 총개수를 알아오고 페이징 처리
df = pd.read_sql("select count(ROWID) AS  count FROM {}".format(table_name) , con = connect)
total_count = df["COUNT"].values[0]
print("total page size : ",total_count)

def save_parquet(cur, query, table_name, while_count ):
    cur.execute(query)

    cols = [column[0] for column in cur.description]
    data = cur.fetchall()

    df = pd.DataFrame(list(data), columns = cols)

    # CLOB TYPE을 string으로 변환
    for c in df.columns:
         if df[c].dtype == object:
             df[c] = df[c].astype("string")

    df = df.drop(labels='RNUM', axis = 1) # 순서번호인 RNUM 삭제
    df.to_parquet('{0}_{1}.parquet'.format(table_name, while_count ) ) # parquet파일 저장

    #CLOB COLUMN 65536byte넘는 ID 필터링
    filtered_df = df[df['ST2'].apply(lambda x: len(str(x).encode("utf-8")) > 65536 )]
    id_df = filtered_df[["ID"]]
    id_df.to_csv('oracle_df_list.txt', mode='a', index=False, header=False)

end_num = start_num + page_size
while_count = 0
while total_count > end_num :
    query = org_query.format( table_schema, table_name, start_num, end_num  )
    #print(query)
    save_parquet(cur, query, table_name, while_count )
    start_num = end_num
    end_num = start_num + page_size
    while_count += 1

connect.close()
