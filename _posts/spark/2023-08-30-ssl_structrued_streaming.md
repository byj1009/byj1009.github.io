---
layout: post
title: "[Spark] Spark Structured Streaming, Kafka to KUDU" #게시물 이름
tags: [spark, spark3, kudu, structured_streaming, kafka, CDC] #태그 설정
categories: spark #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

<https://byj1009.github.io/python/2023/07/25/structured_streaming.html>
Kerberos 보안 설정이 적용이 된 Kafka to Kudu, Spark Structured Streaming을 테스트 이후, Hadoop Ecosystem의 TCP 통신 Layer에 SSL/TLS 보안이 설정되어 있는 경우를 테스트했던 내용을 정리해 본다.   
테스트를 위해서 RootCA와 Host Certs를 Selfsigned로 구성했고, Cloudera Data Platform ~~~Opensource Apache 서비스로 구축하였을 때는 동일한 조건인지는 모르겠다.~~~ 에서 모든 서비스에 사용가능한 JKS 방식의 Truststore를 사용해 구축했다.

# 0. 버전정보
- Linux, Rhel8.6
- Cloudera Data Platform 7.1.7sp2
  - Spark3.2.3.3.2.7172000.0-334
- kerberos enabled
- TLS/SSL enabled

# 1. jaas.conf 작성
kafka consumer를 생성하기 위한 jaas.conf 파일을 생성한다. Apache Ranger를 통해 Hadoop Ecosystem의 Authentication, Authorization을 관리하고 있다면, 관련 Policy를 설정하고 해당 유저의 Keytab을 사용해도 된다.   
>>> Ranger에서 Audit을 관리하고 Resource pool을 적용하기 위해서는 관리자 계정을 별도로 사용하는게 좋은 것 같다.

```bash
KafkaClient {
 com.sun.security.auth.module.Krb5LoginModule required
 useKeyTab=true
 keyTab="/etc/security/keytabs/kafka.keytab"
 storeKey=true
 useTicketCache=false
 serviceName="kafka"
 principal="kafka/test.exmaple.com@EXAMPLE.COM";
};
Client {
  com.sun.security.auth.module.Krb5LoginModule required
  useKeyTab=true
  storeKey=true
  useTicketCache=false
  keyTab="/etc/security/keytabs/kafka.keytab"
  principal="kafka/test.exmaple.com@EXAMPLE.COM";
};
```

# 2. Kafka to Kudu
<https://byj1009.github.io/python/2023/07/25/structured_streaming.html> 기존의 코드에서, TLS/SSL 통신을 위한 Config, Option을 추가해야 한다.   

**체크항목**
- bootstrap_server_info = "bootstrap_server_FQDN:9093"
- Spark Session
  - .config("spark.ssl.enabled", "true") \
  - .config("spark.ssl.keyStore", "/path/to/cert/host_cert.jks") \
  - .config("spark.ssl.keyStorePassword", "password") \
  - .config("spark.ssl.trustStore", "/path/to/cert/jssecacerts") \
  - .config("spark.ssl.trustStorePassword", "password") \
- Kafka Session
  - .option("kafka.security.protocol","SASL_SSL")\
  - .option("kafka.sasl.mechanisms", "GSSAPI")\
  - .option("kafka.ssl.truststore.location","/path/to/cert/host_cert.jks") \
  - .option("kafka.ssl.truststore.password","password") \

``` python
#!/usr/bin/python3
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, when, collect_list
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DecimalType


### 0. kerberos, kafka_topic, kudu_master Info
# kerberos_info
principal_name = "kafka/test.exmaple.com@EXAMPLE.COM"
keytab_location = "/etc/security/keytabs/kafka.keytab"
# Kafka_info
topic = "testtopic"
consumer_group = "cdc_topic_consumer"
bootstrap_server_info = "bootstrap_server_FQDN:9093"
# Kudu_info
kudu_master = "kudu_master_01:7051,kudu_master_02:7051,kudu_master_03:7051"
kudu_table = "cdc.kudu_test"


### 1. Dataframe Schema 정의 / KUDU Table의 schema에 맞게 Dataframe type정의
jsonSchema = StructType([
    StructField("before", StructType([
        StructField("id", IntegerType(), True),
        StructField("val", DecimalType(), True)
    ])),
    StructField("after", StructType([
        StructField("id", IntegerType(), True),
        StructField("val", DecimalType(), True)
    ]))
])

### 2. SparkSession 설정, Kudu Kerberos Session 정보
spark = SparkSession \
    .builder \
    .appName("Kafka_to_Kudu_Streaming") \
    .config("spark.kudu.security.enabled", "true") \
    .config("spark.kudu.security.principal", principal_name) \
    .config("spark.security.credentials.kudu.keytab", keytab_location) \
    .config("spark.ssl.enabled", "true") \
    .config("spark.ssl.keyStore", "/path/to/cert/host_cert.jks") \
    .config("spark.ssl.keyStorePassword", "password") \
    .config("spark.ssl.trustStore", "/path/to/cert/jssecacerts") \
    .config("spark.ssl.trustStorePassword", "password") \
    .getOrCreate()


### 3. kafka Topic data readStream
inputStream = spark.readStream \
  .format("kafka") \
  .option("subscribe", topic) \
  .option("kafka.bootstrap.servers", bootstrap_server_info) \
  .option("kafka.security.protocol","SASL_SSL")\
  .option("kafka.sasl.mechanisms", "GSSAPI")\
  .option("kafka.client.id" ,"Client_ID")\
  .option("kafka.sasl.kerberos.service.name","kafka")\
  .option("kafka.sasl.kerberos.keytab", keytab_location) \
  .option("kafka.sasl.kerberos.principal",principal_name) \
  .option("kafka.ssl.truststore.location","/path/to/cert/host_cert.jks") \
  .option("kafka.ssl.truststore.password","password") \
  .option("startingOffsets", "latest") \
  .option("failOnDataLoss", "false") \
  .load()
#   .option("kafka.group.id", consumer_group) \ # Kafka Consumer Group 명시, 필요시 위에 추가

### 4. Dataframe 생성 
# streamDF = inputStream.selectExpr("CAST(value AS STRING) as kaf_val", "CAST(timestamp as timestamp) as timestamps") \
#     .select(from_json("kaf_val", jsonSchema).alias("jsonData"), "timestamps") \
#     .select("jsonData.*", "timestamps")
streamDF = inputStream.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", jsonSchema) \
    .alias("jsonData")) \
    .select("jsonData.*")
    
### 5. Dataframe 전처리, Status Column(UPSERT, DELETE) 추가
parsedDF = streamDF \
    .withColumn("status",
    when(col("before").isNotNull() & col("after").isNotNull(), "UPSERT")
    .when(col("before").isNull(), "UPSERT")
    .when(col("after").isNull(), "DELETE"))


### 6. Spark To KUDU 함수
def write_to_kudu(df, batchID):
    # 배치에서 데이터를 필터링하여 INSERT, UPDATE, DELETE를 분류하고, 적절한 처리를 수행합니다.
    upsertDF = df.filter(col("status") == "UPSERT").select("after.*")
    deleteDF = df.filter(col("status") == "DELETE").select("before.*")

    # upsert
    upsertDF.write \
        .format("org.apache.kudu.spark.kudu") \
        .option("kudu.master", kudu_master) \
        .option("kudu.table", kudu_table) \
        .option("kudu.operation", "upsert") \
        .mode("append") \
        .save()
    # delete
    deleteDF.write \
        .format("org.apache.kudu.spark.kudu") \
        .option("kudu.master", kudu_master) \
        .option("kudu.table", kudu_table) \
        .option("kudu.operation", "delete") \
        .mode("append") \
        .save()

### 7. foreachBatch를 통한 Structured Streaming
query = parsedDF.writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_kudu) \
    .start()
# 스트리밍 쿼리가 종료될 때까지 대기
query.awaitTermination()

```

# 3. spark 어플리케이션 실행하기
Kerberos가 적용되어 있는 환경이기 때문에, Kerberos Ticket이 만료되면 자동으로 renewal할 수 있도록 옵션을 주어야 한다.   
spark-submit에 deploy-mode를 적용하지 않으면 default로 client 모드로 동작한다. client 모드는 개발/테스트 단계에서 사용하며, prod단계에서는 --deploy-mode를 `cluster`로 적용하여 사용한다.   


추가적으로, Cloudera에서 제공하는 kudu-spark3_2.12.jar파일 이용해서 작업을 했다.

``` bash
#### spark3-submit client mode
spark3-submit --master yarn \
--keytab /etc/security/keytabs/kafka.keytab \
--principal kafka/test.exmaple.com@EXAMPLE.COM \
--jars /opt/cloudera/parcels/CDH/lib/kudu/kudu-spark3_2.12.jar \
--driver-java-options "-Djava.security.auth.login.config=/etc/security/keytabs/jaas.conf" \
--conf "spark.executor.extraJavaOptions=-Djava.security.auth.login.config=/etc/security/keytabs/jaas.conf" \
--conf "spark.driver.extraJavaOptions=-Djava.security.auth.login.config=/etc/security/keytabs/jaas.conf" \
/root/cdctest.py 

#### spark3-submit cluster mode
spark3-submit --deploy-mode cluster \
--keytab /etc/security/keytabs/kafka.keytab \
--principal kafka/test.exmaple.com@EXAMPLE.COM \
--jars /opt/cloudera/parcels/CDH/lib/kudu/kudu-spark3_2.12.jar \
--driver-java-options "-Djava.security.auth.login.config=/etc/security/keytabs/jaas.conf" \
--conf "spark.executor.extraJavaOptions=-Djava.security.auth.login.config=/etc/security/keytabs/jaas.conf" \
--conf "spark.driver.extraJavaOptions=-Djava.security.auth.login.config=/etc/security/keytabs/jaas.conf" \
--conf "spark.yarn.keytab=/etc/security/keytabs/user1.keytab" \
--conf "spark.yarn.principal=user1@GOODMIT.COM" \
--conf "spark.yarn.security.tokens.hive.enabled=false" \
--conf "spark.yarn.security.tokens.hbase.enabled=false" \
/root/cdctest.py 
```


---
### Reference

[apache_spark_document][spark]


[spark]: https://spark.apache.org/docs/latest/running-on-yarn.html