import os

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("sparkstream").getOrCreate()

# Define input sources
# the data is being sent by command  : nc -l 9999
lines = (
    spark.readStream.format("socket")
    .option("host", "localhost")
    .option("port", 9999)
    .load()
)

# Split the lines into words and perform word count
words = lines.select(F.explode(F.split(F.col("value"), "\\s")).alias("word"))
counts = words.groupBy("word").count()

# Configure checkpoint directory
checkpoint_dir = os.path.join(os.getcwd(), "checkpoint")

streamingQuery = (
    counts.writeStream.format("console")
    .outputMode("complete")  # Adjust based on your use case
    .trigger(processingTime="1 second")
    .option("checkpointLocation", checkpoint_dir)
    .start()
)

streamingQuery.awaitTermination()
