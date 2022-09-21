---
layout: post
title: "Kerberized Kafka Cluster" #게시물 이름
tags: [Apache, Clouder, CDP, Kafka, Kerberos, study] #태그 설정
categories: Study #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

Mysql에 Hive metastore DB를 생성하여 hive table을 관리하면, 기본적으로 한글을 사용할 수(글자가 ???로 나옴) 없습니다.

이러한 문제를 해결하기 위해서는 Default Charater set을 latin1에서 UTF8로 변경해야 합니다.

다음의 과정은

# SK hynix Kafka Clustering

# Device Spec

| Host Usage | CPU | Memory | Disk | OS_ver | Install Service |
| --- | --- | --- | --- | --- | --- |
| CM server[Event&User/CDC/M16] 총 3대 | 32 | 128 | 400G | RHEL7.x | Cloudera Manager |
| [통합 HUB] Event Kafka Broker * 5  |  |  | 24T |  | Kafka, Zookeeper, SRM[3대] |
| [통합 HUB] CDC Kafka Broker * 5  |  |  | 24T |  | Kafka, Zookeeper, SRM[3대] |
| [통합 HUB] User Kafka Broker * 5  |  |  | 4T |  | Kafka, Zookeeper |
| [M16 HUB] Event Kafka Broker * 3 |  |  | 4T |  | Kafka, Zookeeper |
| [M16 HUB] CDC Kafka Broker * 3 |  |  | 4T |  | Kafka, Zookeeper |
| [통합 HUB] Schema Registry * 2 |  |  | 400G |  | Schema Registry |
| [통합 HUB - event,cdc,user] Ranger, SMM  |  |  | ? |  | Ranger, Solr, Core Configuration, SMM |
|  |  |  |  |  |  |

<aside>
⚙ Cloudera Manager = 7.1.7
Cloudera Data Platform = 7.4.4
# VM 환경
# MIT Kerberos

</aside>

![kafkaimg.png](SK%20hynix%20Kafka%20Clustering%202385fda9a16541f3a76262c2deb8f064/kafkaimg.png)

<aside>
📢 # LDAP 미구축 >> 계정 별도 관리 ( UNIX )
# Event Cluster 총 partition 20000개 이상 // 1MB 이상 레코드 publishing
# HDFS 대신 Core Configuration 사용
# /etc/security/limits.conf
Data Streaming을 위한 nofile setting
* soft nofile 1048576     >> 128000
* hard nofile 1048576    >> 128000
* soft nproc 6553
* hard nproc 65536
# Posco 프로젝트에서 설정한 값을 이용해 Config를 수정했는데, 터미널 접근이 모두 차단되는 문제가 발생. 65536 or 262144 값이 Cloudera의 권장사항.

</aside>

![Untitled](SK%20hynix%20Kafka%20Clustering%202385fda9a16541f3a76262c2deb8f064/Untitled.png)

```
Streams Replication Manager config
External Kafka Accounts >> Administration/External Accounts에서 Kafka Account 등록 [ 외부 Kafka cluster 정보를 저장해서 일괄 등록을 할 수 있다. Accounts를 등록하거나, Streams Replication Manager's Replication Configs에 직접 입력하여 설정도 가능. ]
Streams Replication Manager Cluster alias : 관리하는 Kafka Broker Cluster의 alias를 붙이며, 복제되는 topic들에는 해당 alias가 붙어 생성된다.

Streams Replication Manager’s Replication Configs :
ehub.bootstrap.servers=xxx.goodmit.co.kr:9092,xxx.goodmit.co.kr:9092, ...
m16.bootstrap.servers=xxx.goodmit.co.kr:9092,xxx.goodmit.co.kr:9092, ...
#복제 방향
m16->ehub.enabled=true
ehub.security.inter.broker.protocol=SASL_PLAINTEXT
ehub.security.protocol=GSSAPI
ehub.sasl.kerberos.service.name = kafka
replication.factor=3
ehub.sasl.jaas.config = com.sun.security.auth.module.Krb5LoginModule required useKeyTab=true keyTab="path/to/keytab file" storeKey=true useTicketCache=false principal="streamsrepmgr@STREAMANALYTICS.COM";
m16.security.protocol=PLAINTEXT

#대용량(1mb 이상) 파일 미러링 세팅
ehub.max.request.size=20971520
ehub.max.partition.fetch.bytes=20971520
m16.max.request.size=20971520    >>20MB
m16.max.partition.fetch.bytes=20971520
## 적용이 정상적으로 되지 않아 다음 설정 추가 // Kafka Mirrormaker2 공식 문서 참조세팅.
ehub.producer.max.request.size=20971520
m16.producer.max.request.size=20971520

Event Cluster, CDC Cluster setting 동일 (bootstrap.servers 정보 제외)
```

<aside>
⚠️ security.inter.broker.protocol 브로커들 사이의 통신 프로토콜
***sasl.mechanism.inter.broker.protocol*** 브로커 간의 통신에 사용할 암호화 알고리즘을 의미한다. GSSAPI, PLAIN, OAUTHBEARER, SCRAM-SHA-256, SCRAM-SHA-512 의 값

</aside>

<aside>
⚠️ #keyTab="/etc/security/keytab/kafka.keytab"

CM에서 자동으로 생성하는 Keytab파일의 디렉토리는 아래와 같고, 해당 kafka.keytab파일을 Kafka broker들에게 (Clustering을 이루는) 특정 디렉토리에 복사한다.
#/var/run/cloudera-scm-agent/process/xx-kafka-KAFKA_BROKER/kafka.keytab 
#mkdir -p /etc/security/keytab
#cp /var/run/cloudera-scm-agent/prcoess/@@-kafka-KAFKA_BROKER/kafka.keytab /etc/security/keytab/

#chmod 644 , chown kafa:kafka
#principal="kafka@xxxxxx.SKHYNIX.COM"  << KDC SERVER Domain
#Kafka Broker 모든 노드에 해당 Keytab파일 배포.

</aside>

Kerberized 카프카 브로커에서 Kafka Broker 테스트

-Kerberos가 적용된 Kafka에서 Kafka관련 command를 사용하기 위해서는 Jaas, [Server.properties](http://Server.properties) 파일을 생성하여 Kerberos관련 설정을 적용해야 한다.(CLI)

```bash
#####      jaas.conf  생성  #####
KafkaServer {
    com.sun.security.auth.module.Krb5LoginModule required
    useKeyTab=true
    storeKey=true
    keyTab="~/kafka.keytab"
    principal="kafka@EXAMPLE.COM";
};

#####       server.properties  생성    ###### 
security.inter.broker.protocol=SASL_PLAINTEXT
sasl.kerberos.service.name=kafka

# List of enabled mechanisms, can be more than one
sasl.enabled.mechanisms=GSSAPI
# Specify one of of the SASL mechanisms
sasl.mechanism.inter.broker.protocol=GSSAPI

jaas.conf 파일 적용
$ export KAFKA_OPTS="-Djava.security.auth.login.config=~/jaas.conf"
```

kafka 동작 테스트

```bash
# Kafka Test Command
# Kafka topic 생성
$ kafka-topics --create --topic <topic name> --bootstrap-server <kafka broker IP>:9092 --server

1.	Kafka producer, kafka consumer record 생성 및 확인
kafka-console-producer --topic test-topics --bootstrap-server <kafka broker IP>:9092
kafka-console-consumer --topic test-events --bootstrap-server <kafka broker IP>:9092
```

Kerberos, TLS 세팅에 따른 Protocol

| Kerberos or LDAP enabled | TLS/SSL enabled | Protocol |
| --- | --- | --- |
| YES | YES | SASL_SSL |
| YES | NO | SASL_PLAINTEXT |
| NO | YES | SSL |
| NO | NO | PLAINTEXT |

SRM 명령어

CM에서 설정한 Secure storage password를 CLI에서 선언한 후에 SRM명령어를 사용해야 한다.

미러링 정책을 생성하고 적용하는 것은 모두 CLI에서 작업을 해야 한다.

```
$export [***SECURE STORAGE ENV VAR***]=”[***SECURE STORAGE PASSWORD***]”
```

```bash

#Add topics or groups to an allowlist:
srm-control topics --source [SOURCE_CLUSTER] --target [TARGET_CLUSTER] --add [TOPIC1],[TOPIC2]
```

KAFKA, Streaming Replication Service(SRM) 명령어 모음

```
1) 토픽 생성
$kafka-topics --create \

- -bootstrap-server [my-kafka]:9092 \
- -topic [토픽 이름]
- -partitions [생성할 파티션 수] \
- -replication-factor [브로커 복제 계수] \
- -config retention.ms=[토픽의 데이터를 유지할 시간 (단위: ms)]

2) 토픽 리스트 조회
$kafka-topics --bootstrap-server [my-kafka]:9092 --list

3) 특정 토픽 상세 조회
$kafka-topics --bootstrap-server [my-kafka]:9092 --topic [조회할 토픽 이름] --describe

4) 토픽 수정
$kafka-topics --bootstrap-server [my-kafka]:9092 --alter \
--partitions [변경할 파티션 수]
--add-config retention.ms=[토픽의 데이터를 유지할 시간 (단위: ms)]
기존에 없는 옵션이면 신규로 추가하고, 기존에 존재하는 옵션이면 값을 변경한다.
--delete-config retention.ms
토픽 설정 삭제

5) 토픽의 레코드 삭제
$kafka-delete-records --bootstrap-server [my-kafka]:9092 --offset-json-file delete-topic.json
```

> 5-1) json 파일을 활용한 레코드 삭제

vi delete-topic.json 과 같은 명령으로 json 파일을 생성한다. (파일명은 자유롭게)
-- delete-topic.json
{
  "partitions": [
    {
      "topic": "[삭제할 레코드가 있는 토픽명]",
      "partition": [삭제할 레코드가 있는 파티션 번호],
      "offset": [처음부터 삭제할 offset 번호]
    }
  ],
  "version": 1 
}
> 

```
Kafka Producer
1) 레코드 produce

1-a) key가 없고 value만 있는 메시지 produce

$kafka-console-producer --boostrap-server [my-kafka]:9092 --topic [레코드를 저장할 토픽명]

1-b) key와 value가 있는 메시지 produce

$kafka-console-producer --boostrap-server [my-kafka]:9092 --topic [레코드를 저장할 토픽명] \

- -property "parse.key=true" \
- -property "key.separator=:"

*※ 메시지를 입력할때, 콜론을 사용하여 key:value 형태로 입력하도록 하려면 아래와 같이 명령어를 작성할 수 있다.*
```

```
kafka Consumer
1) 레코드 consume

1-a) key 없이 value만 보여주는 consume

$kafka-console-consumer --bootstrap-server my-kafka:9092 --topic [레코드를 읽어 올 토픽명]

- -from-beginning

*from-beginning 옵션은 토픽에 저장된 가장 첫 데이터부터 읽어온다.*

1-b) key와 value를 보여주는 consume

$kafka-console-consumer --bootstrap-server my-kafka:9092 \

- -topic [레코드를 읽어 올 토픽명] \
- -property print.key=true \
- -property key.separator="-" \
- -group [이 컨슈머가 속할 그룹명 (지정한 그룹명이 없는 경우 새로 생성됨)] \
- -from-beginning

*property print.key=true를 사용하여 메시지 키를 노출 시킬 수 있다. property key.separator="-"를 사용하여 key와 value를 하이픈(-)으로 분리해서 보여줄 수 있다. group [그룹명]을 사용하여 이 컨슈머의 컨슈머 그룹을 지정 또는 생성할 수 있다.*

2) Cosumer group

2-a) 컨슈머 그룹에 속하는 컨슈머 리스트 조회

$kafka-consumer-groups --bootstrap-server [my-kafka]:9092 --list

2-b) 컨슈머 그룹이 어떤 토픽의 데이터를 처리하는지 조회

$kafka-consumer-groups --bootstrap-server [my-kafka]:9092 \

- -group [존재하는 컨슈머 그룹명]
- -describe

*컨슈머 그룹명, 컨슘하고 있는 토픽명, 컨슘하고 있는 토픽의 파티션 번호, 컨슈머 그룹이 가져간 토픽의 파티션의 최신 오프셋, 컨슈머 그룹의 컨슈머가 컨슘한 오프셋, 컨슈머 그룹이 토픽의 파티션에 있는 데이터를 가져가는데 발생하는 지연. 랙(LAG), 컨슈머 아이디 등을 알 수 있다.*
```

```
SRM명령어
Add topics or groups to an allowlist:
srm-control topics --source [SOURCE_CLUSTER] --target [TARGET_CLUSTER] --add [TOPIC1],[TOPIC2]
srm-control groups --source [SOURCE_CLUSTER] --target [TARGET_CLUSTER] --add [GROUP1],[GROUP2]
Remove topics or groups from an allowlist:
srm-control topics --source [SOURCE_CLUSTER] --target [TARGET_CLUSTER] --remove [TOPIC1],[TOPIC2]
srm-control groups --source [SOURCE_CLUSTER] --target [TARGET_CLUSTER] --remove [GROUP1],[GROUP2]
Add topics or groups to a denylist (blacklist):
srm-control topics --source [SOURCE_CLUSTER] --target [TARGET_CLUSTER] --add-blacklist [TOPIC1],[TOPIC2]
srm-control groups --source [SOURCE_CLUSTER] --target [TARGET_CLUSTER] --add-blacklist [GROUP1],[GROUP2]
Remove topics or groups from a denylist:
srm-control topics --source [SOURCE_CLUSTER] --target [TARGET_CLUSTER] --remove-blacklist [TOPIC1],[TOPIC2]
srm-control groups --source [SOURCE_CLUSTER] --target [TARGET_CLUSTER] --remove-blacklist [GROUP1],[GROUP2]
Specifying topics or groups is also possible with regular expressions. The following example adds all topics to the allowlist, meaning that every topic on the source cluster will be replicated to the target cluster.
srm-control topics --source [SOURCE_CLUSTER] --target [TARGET_CLUSTER] --add ".*"
In addition to adding or removing items, you can also use the tool to look at the contents of a deny or allowlist.
srm-control topics --source [SOURCE_CLUSTER] --target [TARGET_CLUSTER] --list

srm-control --bootstrap-servers localhost:9092 topics --source [SOURCE_CLUSTER] --target [TARGET_CLUSTER] --list
Alternatively, you can also use the --props option together with the bootstrap.servers Kafka property to define the bootstrap server.
srm-control --props bootstrap.servers=localhost:9092 topics --source [SOURCE_CLUSTER] --list
```

```
Kafka Test Command
0.	Kafka topic 생성
kafka-topics --create --topic test-events2 --bootstrap-server kafka01:9092 --partitions 3 --replication-factor 3

1.	Kafka producer, kafka consumer record 생성 및 확인
kafka-console-producer --topic test-topics --bootstrap-server kafka01:9092
kafka-console-consumer --topic test-events --from-beginning --bootstrap-server kafka01:9092
```

Solr-infra Time to Live 변경하는 방법

[https://docs.cloudera.com/cloudera-manager-ibm/7.2.3/installation/topics/cdpdc-additional-steps-ranger.html](https://docs.cloudera.com/cloudera-manager-ibm/7.2.3/installation/topics/cdpdc-additional-steps-ranger.html)