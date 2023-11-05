---
layout: post
title: "[Airflow] Linux, Rhel8에 Apache Airflow 설치하기" #게시물 이름
tags: [python, apache, airflow, Linux, Rhel8, airflow2.7.0] #태그 설정
categories: Airflow #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

Hadoop Ecosystem에서 Apache Spark의 학습을 진행하며 Scheduling을 위해 Apache Airflow2.7.0을 Rhel8.6 환경에 구축하는 과정을 정리해본다.

# Prerequisites
아래는 Apache Airflow 공식 사이트에서 명시하는 관련 서비스들의 버전 정보다.   
<https://airflow.apache.org/docs/apache-airflow/stable/installation/prerequisites.html>

- Python: 3.8, 3.9, 3.10, 3.11
- Databases:
	- PostgreSQL: 11, 12, 13, 14, 15
	- MySQL: 5.7, 8
	- SQLite: 3.15.0+
	- MSSQL(Experimental): 2017, 2019
- Kubernetes: 1.23, 1.24, 1.25, 1.26, 1.27

MySQL기반의 MariaDB에서는 Known Issue들이 존재하기 때문에, 사용하지 않는 것을 권장하고 있으며, 기본으로 내장되어 있는 SQLite 또한 테스트용으로 만 사용하며 Production 레벨에서는 사용하지 않는 것을 권하고 있다.

이러한 이유로, Postgresql14를 이용해 Apache Airflow 설치를 진행할 것이고, 관련 설치에 대한 내용은 다루지 않는다~~.

# Apache Airflow Install

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
