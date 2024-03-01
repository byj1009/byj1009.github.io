import sys
from pyspark.sql import SparkSession, Row
from pyspark.sql.function import col, from_json, when, expr, struct, lit, concat, md5, regexp_replace, udf
from pyspark.sql.types import *
import py_psql

# connection Info
principal_name = "tester@example.co.kr"
keytab_location = "/path/location/tester.keytab"

ora_table_info = sys.argv[1].upper()
ora_schema, ora_table = ora_table_info.split(".")[0], ora_table_info.split(".")[1]

kafka_startingOffset = "{\"" + ora_schema + "." + ora_table + "\":{\"0\":" + sys.argv[2] + "}}" if len(sys.argv) > 2 else "latest"
bootstrap_server_info = "server01.example.co.kr,server2...."

kudu_table = ora_table_info.lower()
kudu_master = 'server01.example.co.kr:7051,server02....:7051, ...'

# py_psql.py 함수 호출
query_results = py_psql.execute_query(kudu_table.split(".")[0],kudu_table.split(".")[1])
FIRST_COLUMN = query_results[0][0]

# clob, tmp_pk 생성
clob_columns = py_psql.clob_column_check(ora_schema, ora_table)
tmppk_columns = py_psql.check_table_name(ora_schema, ora_table)

# Scehma parsing
bf_md5_hashing_str, af_md5_hashing_str = py_psql.convert_to_spark_schema_no_pk(query_results,tmppk_columns)
spark_schema_str, casewhen_schema, bf_schema_str, af_schema_str = py_psql.convert_to_spark_schema(query_results, clob_columns)
udf_scehma_str, udf_schema_tmp_str = py_psql.udf_spark_schema(query_results)

#1. DataFrame 정의
jsonSchema = StructType([
                    StructField("metadata", StructType([StructField("committimestamp", TimestampType())])),
                    StructField("before", StructType(eval(f"[{spark_schema_str}]"))),
                    StructField("after", StructType(eval(f"[{spark_schema_str}]")))
            ])

#2. SparkSession Info
spark = SparkSession.builder \
                    .appName(f"{kudu_table}_streaming") \
                    .config("spark.kudu.security.enabled", "true") \
                    .config("spark.kudu.security_principal", principal_name) \
                    .config("spark.kudu.security.credentials.kudu.keytab", keytab_location) \
                    .config("spark.sql.session.timeZone", "UTC") \
                    .config("spark.sql.autoBroadcastJoinThreshold", "-1") \
                    .getOrCreate()

spark.sparkcontext.setLogLevel("WARN")
spark.conf.set("spark.sql.execution.arrow.pyspark.fallback.enabled","false")

#3. Kafka Topic Data Read Streaming
inputStream = spark.readStream \
                   .format("kafka") \
                   .option("subscribe", ora_table_info) \
                   .option("kafka.bootstrap.servers", bootstrap_server_info) \
                   .option("kafka.security.protocol","SASL_PLAINTEXT") \
                   .option("kafka.sasl.mechanism","GSSAPI") \
                   .option("kafka.client.id","KafkaClient") \
                   .option("kafka.sasl.kerberos.service.name","kafka") \
                   .option("kafka.sasl.kerberos.keytab", keytab_location) \
                   .option("kafka.sasl.kerberos..principal", principal_name) \
                   .option("startingOffsets", kafka_startingOffset) \
                   .option("failOnDataLoss", "false") \
                   .load()


#4. DataFrame 생성
streamDF = inputStream.selectExpr("CAST(value AS STRING)") \
                      .select(from_json("value", jsonSchema).alias("jsonData")) \
                      .select("jsonData.*")

#5. Parsing Data
parsedDF = streamDF.withColumn("operation",when(col("before").isNull,"insert_ignore")
                                          .when(col("after").isNull, "delete_ignore")
                                          .otherwise("upsert"))

#5-1. Primary 생성
if FIRST_COLUMN == "tmp_pk":
    parsedDF = parsedDF.withColumn("before",when(col("before").isNotNull(), eval(f"""struct({bf_schema_str})"""))) \
                       .withColumn("after",when(col("after").isNotNull(), eval(f"""struct({af_schema_str})"""))) \
                       .withColumn("before", expr(f"""named_struct({bf_md5_hashing_str})""")) \
                       .withColumn("after", expr(f"""named_struct({af_md5_hashing_str})"""))
else:
    parsedDF = parsedDF.withColumn("before",when(col("before").isNotNull(), eval(f"""struct({bf_schema_str})"""))) \
                       .withColumn("after",when(col("after").isNotNull(), eval(f"""struct({af_schema_str})"""))) \

# After에 Primary Key column 값 Null 채우기
parsedDF = parsedDF.withColumn("after",
                                    expr(f"""CASE WHEN operation = 'upsert'
                                             THEN struct({casewhen_schema_str})
                                             ELSE after
                                             END"""
                                ))

#6. Streaming process fucntion
def select_data(operation, before, after):
    if operation == "delete_ignore":
        return before
    else:
        return after

udfSchema = StructType(eval(f"[{udf_schema_str}]"))
udftmpSchema = StructType(eval(f"[{udf_scehma_tmp_str}]"))

select_data_udf = udf(select_data, udfSchema)

def size_in_bytes(s):
    if s is None:
        return 0
    return len(s.encode('utf-8'))

size_in_bytes_udf = udf(size_in_bytes, IntegerType())

parsedDF = parsedDF.withColumn("data", select_data_udf(col("operation"), col("before"), col("after"))) \
                   .select(col("data.*"), col("metadata.committimestamp"), col("operation").alias("operation"))

# kudu write function
def kudu_write_func(df, dml_oper, table_name):
    df.write \
      .format("org.apache.kudu.spark.kudu") \
      .option("kudu.master", kudu_master) \
      .option("kudu.table", table_name) \
      .option("kudu.operation", dml_oper) \
      .option("kudu.ignoreNull", True) \
      .mode("append") \
      .save()

def write_to_kudu(df, batchID):
    # 각 row에 대한 순차처리
    for row in df.collection():
        operation = row["operation"]

        tmpDF = spark.createDataFrame([row], udfSchema)
        kudu_write_func(tmpDF.select(tmpDF.columns[:01]), operation, kudu_table)

    deleteDF = df.filter(col("operation" == "delete_ignore").select(df.columns[:-1])
    deleteDF = deleteDF.selectExpr(f"md5(concat({FIRST_COLUMN}, '{kudu_table}')) as tmp_pk"
                                  ,f"'{kudu_table}' as table_name"
                                  ,f"cast({FIRST_COLUMN} as string) as deleted_record_pk"
                                  ,'committimestamp as committimestamp')
    
    kudu_write_func(deleteDF, "UPSERT", logging_kudu_table)


#7. 스트리밍 쿼리 실행
if clob_columns:
    # 65535byte가 넘는 문자열에 한하여 숫자, 영어, 한글, 특수문자(ASKII) 이외 문자 제거, 길이 자르기
    for clob_col in clob_columns:
        parsedDF = parsedDF.withColumn(clob_col, when(size_in_bytes_udf(col(clob_col)) > 65535
                                                    ,concat(lit('<transformed data>'), regexp_replace(col(clob_col),"[^\x00-\x7F가-힣]+","")))
                                                    .otherwise(col(clob_col))) \
                                                    .withColumn(clob_col, expr(f"encode({clob_col}, 'utf-8')")) \
                                                    .withColumn(clob_col, expr(f"substring({clob_col}, 1, 65535)")) \
                                                    .withColumn(clob_col, expr(f"decode({clob_col}, 'utf-8')"))

    query = parsedDF.writeStream \
                    .outputMode("append")
                    .foreachBatch(write_to_kdu) \
                    .option("checkpointLocation", f"hdfs://nameservice/tmp/spark/{kudu_table}_checkpoint") \
                    .start()
else:
    query = parsedDF.writeStream \
                    .outputMode("append")
                    .foreachBatch(write_to_kdu) \
                    .option("checkpointLocation", f"hdfs://nameservice/tmp/spark/{kudu_table}_checkpoint") \
                    .start()

query.awaitTermination()
