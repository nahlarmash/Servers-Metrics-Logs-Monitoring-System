from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, col, window, to_timestamp

spark = SparkSession.builder \
    .appName("KafkaLogProcessor") \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop-namenode:9000") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Read Kafka stream
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-1:9092") \
    .option("subscribe", "test-topic3") \
    .option("startingOffsets", "latest") \
    .load()

# Extract fields using updated regex
logs_df = df.selectExpr("CAST(value AS STRING) as raw_log") \
    .withColumn("timestamp_str", regexp_extract(col("raw_log"), r"\[\w{3}, (\d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2}) GMT\]", 1)) \
    .withColumn("method", regexp_extract(col("raw_log"), r"\] (\w+)", 1)) \
    .withColumn("endpoint", regexp_extract(col("raw_log"), r"\] \w+ ([^\s]+)", 1)) \
    .withColumn("response_code", regexp_extract(col("raw_log"), r" (\d{3}) \d+$", 1)) \
    .withColumn("timestamp", to_timestamp(col("timestamp_str"), "dd MMM yyyy HH:mm:ss")) \
    .drop("timestamp_str")

# Windowed aggregation
windowed_counts = logs_df \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(window(col("timestamp"), "5 minutes"), col("method"), col("response_code")) \
    .count()

# Write to HDFS
query = windowed_counts.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "hdfs://hadoop-namenode:8020/user/spark/output") \
    .option("checkpointLocation", "hdfs://hadoop-namenode:8020/user/spark/checkpoint") \
    .start()

query.awaitTermination()
