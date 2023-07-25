---
layout: post
title: "[Python] kafka-python을 통한 실시간 kudu cdc" #게시물 이름
tags: [pyhton, Kafka, kudu, consumer, 카프카, CDC] #태그 설정
categories: python #카테고리 설정
author: # 작성자
  - Byungineer
#toc : true #Table of Contents
---

<https://byj1009.github.io/python/2023/07/25/python-kafka2.html>
python이 아닌 CDC를 위한 데이터 파이프라인(spark, flink, redis, ...) 중 Spark Structured Streaming을 통해 구현을 해보고자 한다.   
앞서 Python을 통해 구현했던 것과 같이 Kerberos 보안 정책이 적용된 환경이며, 빅데이터 플랫폼은 Cloudera 기반으로 구축되었다.   
추가적으로, Structured Streaming은 Spark3부터 지원하므로 Cloudera Data Flatform에 추가 서비스 설치 작업이 필요하다.

# 0. 버전정보
- Linux, Rhel8.6
- Cloudera Data Platform 7.1.7sp2
  - Spark3.2.3.3.2.7172000.0-334
- kerberos enabled

# 1. Pyspark 코드 작성
## 1.1 예제 코드 실행하기 Pi

spark-example.jar를 이용해서 Spark3의 기능테스트를 해볼 수 있다. Kerberos가 적용된 환경이기 때문에, 관련 Authorization 설정이 된 Keytab, Principal 정보가 필요로 함.   
관련 설정을 Cloudera Data Platform에서는 관련 Policy를 Apache Ranger를 통해서 설정 가능.   
Ranger 설정 내용은 따로 다루지 않겠으나, HDFS, Kafka, Spark에 대한 Policy 정책을 살펴보면 쉽게 적용이 가능할 것이다.

HDFS에는 /user/spark 아래에 .application이라는 tmp 디렉토리가 생성되며 관련 로그 및 임시 파일들이 저장되기 때문에 권한이 필요로 함.

```bash
spark3-submit --class org.apache.spark.examples.SparkPi \
    --num-executors 1 \
    --driver-memory 512m \
    --executor-memory 512m \
    --executor-cores 1 \
    --principal [PRINCIPAL] \
    --keytab [KEYTAB_Location] \
    $PATH/spark-examples_2.11-2.4.7.7.1.7.2000-305.jar \
    10
```
## 1.2 kafka_to_kudu.py 파일

테스트용 Stream input data, kudu table schema는 아래와 같다. 

data = {"before":{
                "id": [int],
                "val": [decimal]
                },
        "after":{
            "id": [int],
            "val": [decimal]
                }
        }

| Column (2) | Type | Sample |
| --- | --- | --- |
| id  | int |   1 |
| val | decimal(9,0) | 2000 |

kafka의 topic record를 inputStream Dataframe에 담았을 때의 정보는 다음과 같다. **테스트 용이라 key 값을 따로 주지 않음
+----+--------------------+---------+---------+------+--------------------+-------------+
| key|               value|    topic|partition|offset|           timestamp|timestampType|
+----+--------------------+---------+---------+------+--------------------+-------------+
|null|[7B 22 61 66 74 6...|cdctopic |        0| 10906|2023-07-24 14:57:...|            0|
|null|[7B 22 61 66 74 6...|cdctopic |        0| 10907|2023-07-24 14:57:...|            0|
|null|[7B 22 61 66 74 6...|cdctopic |        0| 10908|2023-07-24 14:57:...|            0|
|null|[7B 22 61 66 74 6...|cdctopic |        0| 10909|2023-07-24 14:57:...|            0|
+----+--------------------+---------+---------+------+--------------------+-------------+

``` python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, when, collect_list
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DecimalType


### 0. kerberos, kafka_topic, kudu_master Info
# kerberos_info
principal_name = "test@REALM.COM"
keytab_location = "/etc/security/keytabs/test.keytab"
# Kafka_info
topic = "cdctopic"
consumer_group = "cdc_topic_consumer"
bootstrap_server_info = "bootstrap_server_IP:9092"
# Kudu_info
kudu_master = "kudu_master01_IP:7051,kudu_master02_IP:7051,kudu_master03_IP:7051"
kudu_table = "testdb.cdc_table"


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
    .getOrCreate()

### 3. kafka Topic data readStream
inputStream = spark.readStream \
  .format("kafka") \
  .option("subscribe", topic) \
  .option("kafka.bootstrap.servers", bootstrap_server_info) \
  .option("kafka.security.protocol","SASL_PLAINTEXT")\
  .option("kafka.sasl.mechanisms", "GSSAPI")\
  .option("kafka.client.id" ,"Client_ID")\
  .option("kafka.sasl.kerberos.service.name","kafka")\
  .option("kafka.sasl.kerberos.keytab", keytab_location) \
  .option("kafka.sasl.kerberos.principal",principal_name) \
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

Spark가 Kerberized Kafka Broker에 대한 Connection을 하기 위해서 spark3-submit 옵션에 관련 정보를 명시해야 하고, Spark와 Kudu Connection을 위해서 SparkSession에 관련 설정 정보를 작성해야 한다.   
또한, Spark3-submit의 동작 방식에는 client, cluster, local mode가 존재하며 Kerberos 보안이 적용되어 있을 경우에는 조금은 다르게 설정을 해주어야 한다.   
관련 포스팅은 따로 다루도록 하겠다.

**foreachBatch**   
foreachBatch를 이용한 Micro-batch를 순차적으로 처리할 수 있다. micro-batch는 스트림데이터를 1초 단위로(Default설정, option을 통해서 변경 가능.) Dataframe을 잘라서 처리를 한다.   
Change Data Capture의 경우에는 순차성 보장이 매우 매우 중요하기 때문에 micro-batch가 병렬로 처리되어 순차성이 깨지는 것을 방지해야 한다.   
foreachBatch를 사용해서 Console에 출력을 해서 내용을 살펴보면, micro-batch에 batchID가 붙어 순차적으로 처리되는 것을 확인할 수 있다.


# 2. spark 어플리케이션 실행하기
Kerberos가 적용되어 있는 환경이기 때문에, Kerberos Ticket이 만료되면 자동으로 renewal할 수 있도록 옵션을 주어야 한다.   
spark-submit에 deploy-mode를 적용하지 않으면 default로 client 모드로 동작한다. client 모드는 개발/테스트 단계에서 사용하며, prod단계에서는 --deploy-mode를 `cluster`로 적용하여 사용한다.   

아래의 코드 예시와 같이 client mode와 cluster모드에서의 옵션 정보가 달라지며, client 모드로 작업시에는 해당 linux Session에서 Kafka, Spark, Kudu 관련 Ranger Policy가 적용된 Keytab으로 `kinit`이 필요하다.   


추가적으로, Cloudera에서 제공하는 kudu-spark3_2.12.jar파일 이용해서 작업을 했다.

``` bash
#### spark3-submit client mode
spark3-submit --master yarn --keytab /etc/security/keytabs/tester1.keytab --principal tester1@GOODMIT.COM \
--jars /opt/cloudera/parcels/CDH/lib/kudu/kudu-spark3_2.12.jar \
--driver-java-options "-Djava.security.auth.login.config=/etc/security/keytabs/jaas.conf" \
--conf "spark.executor.extraJavaOptions=-Djava.security.auth.login.config=/etc/security/keytabs/jaas.conf" \
--conf "spark.driver.extraJavaOptions=-Djava.security.auth.login.config=/etc/security/keytabs/jaas.conf" \
/root/spark/kafka.py 

#### spark3-submit cluster mode
spark3-submit --deploy-mode cluster \
--keytab /etc/security/keytabs/tester1.keytab \
--principal tester1@GOODMIT.COM \
--jars /opt/cloudera/parcels/CDH/lib/kudu/kudu-spark3_2.12.jar \
--driver-java-options "-Djava.security.auth.login.config=/etc/security/keytabs/jaas.conf" \
--conf "spark.driver.extraJavaOptions=-Djava.security.auth.login.config=/etc/security/keytabs/jaas.conf" \
--conf "spark.executor.extraJavaOptions=-Djava.security.auth.login.config=/etc/security/keytabs/jaas.conf" \
--conf "spark.yarn.keytab=/etc/security/keytabs/tester1.keytab" \
--conf "spark.yarn.principal=tester1@GOODMIT.COM" \
--conf "spark.yarn.security.tokens.hive.enabled=false" \
--conf "spark.yarn.security.tokens.hbase.enabled=false" \
/root/spark/kafka.py 
```



# Extra, Console 출력
Dataframe이 어떻게 나오는지 terminal에 출력을 해보고 싶으면, 아래와 같이 `.format("console")` 을 적용하면 된다.

``` python

# console 출력
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, when, collect_list
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DecimalType


### 0. kerberos, kafka_topic, kudu_master Info
principal_name = "test@REALM.COM"
keytab_location = "/etc/security/keytabs/test.keytab"
topic = "cdctopic"
consumer_group = "cdc_topic_consumer"
bootstrap_server_info = "bootstrap_server_IP:9092"
kudu_master = "kudu_master01_IP:7051,kudu_master02_IP:7051,kudu_master03_IP:7051"
kudu_table = "testdb.cdc_table"

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
    .getOrCreate()

### 3. kafka Topic data readStream
inputStream = spark.readStream \
  .format("kafka") \
  .option("subscribe", topic) \
  .option("kafka.bootstrap.servers", bootstrap_server_info) \
  .option("kafka.security.protocol","SASL_PLAINTEXT")\
  .option("kafka.sasl.mechanisms", "GSSAPI")\
  .option("kafka.client.id" ,"Client_ID")\
  .option("kafka.sasl.kerberos.service.name","kafka")\
  .option("kafka.sasl.kerberos.keytab", keytab_location) \
  .option("kafka.sasl.kerberos.principal",principal_name) \
  .option("startingOffsets", "latest") \
  .option("failOnDataLoss", "false") \
  .load()

### 4. Dataframe 생성 
streamDF = inputStream.selectExpr("CAST(value AS STRING) as kaf_val", "CAST(timestamp as timestamp) as timestamps") \
    .select(from_json("kaf_val", jsonSchema).alias("jsonData"), "timestamps") \
    .select("jsonData.*", "timestamps")

### 5. Dataframe 전처리, Status Column(UPSERT, DELETE) 추가
parsedDF = streamDF \
    .withColumn("status",
    when(col("before").isNotNull() & col("after").isNotNull(), "UPSERT")
    .when(col("before").isNull(), "UPSERT")
    .when(col("after").isNull(), "DELETE"))
### Console 출력
query = parsedDF \
     .writeStream \
     .outputMode("append") \
     .format("console") \
     .start() \
query.awaitTermination()
```




---
### Reference

[apache_spark_document][spark]


[spark]: https://spark.apache.org/docs/latest/running-on-yarn.html