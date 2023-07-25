---
layout: post
title: "[Python] Python으로 Kafka Producer 구현" #게시물 이름
tags: [pyhton, Kafka, Topic, Producer, producing, 카프카] #태그 설정
categories: python #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

















``` python
#! /usr/bin/python3
from impala.dbapi import connect
from kafka import KafkaConsumer
from krbcontext.context import krbContext
import json

### 변수
bootstrap_server = ['cfm01.goodmit.com:9092']
topic_name = "cdc_topic2"
consumer_group_name = "cdc_test_group"
table_name = "testdb.cdc_table2"

with krbContext(using_keytab=True, principal='tester1@GOODMIT.COM', keytab_file='/etc/security/keytabs/tester1.keytab', ccache_file='/tmp/krb5cc_pid_nifi_test'):
    conn = connect(
        host="cdp02.goodmit.com",
        port=21050,
        auth_mechanism='GSSAPI',
        kerberos_service_name="impala"
    )
    cursor = conn.cursor()

    try:
        consumer = KafkaConsumer(
            topic_name,
            group_id=consumer_group_name,
            bootstrap_servers=bootstrap_server,
            enable_auto_commit=True,
            auto_offset_reset='earliest',
            sasl_mechanism='GSSAPI',
            security_protocol='SASL_PLAINTEXT',
            sasl_kerberos_service_name='kafka'
        )
        # 토픽 레코드 (cdc 트랜잭션 로그) 읽기
        for message in consumer:
            parsed_data = json.loads(message.value)  # 토픽 메시지를 JSON 형식으로 로드합니다.

            # 초기화
            primary_key_val = 0
            update_val = 0

            # IMPALA를 사용한 UPDATE 쿼리
            if "before" in parsed_data and "after" in parsed_data:
                for key, value in parsed_data["after"].items():
                    if key == "id":
                        primary_key_val = value
                    elif key == "val":
                        update_val = value
                cursor.execute("UPDATE %s SET val=%d WHERE id=%d" % (table_name, update_val, primary_key_val))

            # IMPALA를 사용한 DELETE 쿼리
            elif "before" in parsed_data:  # DELETE
                for key, value in parsed_data["before"].items():
                    if key == "id":
                        primary_key_val = value
                cursor.execute("DELETE FROM %s WHERE id=%d" % (table_name, primary_key_val))

            # IMPALA를 사용한 INSERT 쿼리
            elif "after" in parsed_data:  # INSERT
                for key, value in parsed_data["after"].items():
                    if key == "id":
                        primary_key_val = value
                    elif key == "val":
                        update_val = value
                cursor.execute("INSERT INTO %s VALUES (%d, %d)" % (table_name, primary_key_val, update_val))

    except Exception as e:
        print("An error occurred:", str(e))

    cursor.close()
    conn.close()
```





---
### Reference
[https://ko.wikipedia.org][wikipedia-link]
[[https://m.blog.naver.com/pisibook][https://m.blog.naver.com/pisibook]
[https://soooprmx.com][https://soooprmx.com/]



[wikipedia-link]: https://ko.wikipedia.org/wiki/%EA%B3%A0%EA%B8%89_%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D_%EC%96%B8%EC%96%B4
[https://m.blog.naver.com/pisibook]: https://m.blog.naver.com/pisibook/221711169180
[https://soooprmx.com/]: https://soooprmx.com/%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%9D%80-%EC%9D%B8%ED%84%B0%ED%94%84%EB%A6%AC%ED%84%B0%EC%96%B8%EC%96%B4%EC%9E%85%EB%8B%88%EA%B9%8C/
