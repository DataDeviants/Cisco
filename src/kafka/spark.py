from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql import SparkSession

KAFKA_TOPIC_NAME = "test"
KAFKA_BOOTSTRAP_SERVER = "localhost:29092"

spark = SparkSession.builder \
    .appName("Kafka Stream Reader") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# Read Stream from your Kafka topic
sampleDataframe = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER)
    .option("subscribe", KAFKA_TOPIC_NAME)
    .option("startingOffsets", "latest")
    .load()
)

# read from kafka topic and convert value to json
sampleDataframe = sampleDataframe.selectExpr("CAST(value AS STRING)")
sampleDataframe = sampleDataframe.select(from_json(
    "value", "tag STRING, name STRING, index INT, score MAP<STRING, INT>").alias("data"))

# print the schema of the dataframe
sampleDataframe.printSchema()

# write the dataframe to console
query = sampleDataframe.writeStream.outputMode(
    "append").format("console").start()

query.awaitTermination()
