# script code
from pyspark.sql import SparkSession
import re

def process_line(line):
    line = line.strip()
    line = re.sub(r'\t', '', line)
    line = re.sub(r'[^\w\s]', '', line)
    
    words = line.split(" ")
    return [word.lower() for word in words if word]

if __name__ == "__main__":
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("WordCount") \
        .getOrCreate()

    sc = spark.sparkContext

    ts_spark = sc.textFile("/user/hadoop/taylor_lyrics/*")
    
    # Process and tokenize lines
    ts_tokens = ts_spark.flatMap(process_line)

    # Filter out empty strings
    ts_tokens = ts_tokens.filter(lambda x: x != '')

    # Map each word to (word, 1)
    ts_count = ts_tokens.map(lambda word: (word, 1))

    # Reduce by key to get Word Count
    ts_wc = ts_count.reduceByKey(lambda x, y: x + y)

    # Format the output without parentheses, commas, and colons
    ts_output = ts_wc.map(lambda x: f"{x[0]}\t{x[1]}")

    # Save the formatted Word Count results to HDFS
    ts_output.saveAsTextFile('/user/hadoop/results/hadoop_mapreduce_spark')

    # Stop the Spark context
    sc.stop()
