# About this
Hadoop Distributed File System and MapReduce were used to identify and calculate the word count for lyrcis of all Taylor Swift's songs.

# Background
The whole system runs on a cluster of AWS EC2 instances with the SunU-Hadoop-Image v1.3 AMI, where it is configured with 1 master node and 3 slave nodes.

## How to run?
1. Ensure you have configured EC2 clusters accordingly with MapReduce and HDFS.
```
# Check if its empty
hadoop fs -ls /

# Create a new directory in HDFS for your assignment
hadoop fs -mkdir /user
hadoop fs -mkdir /user/hadoop
hadoop fs -mkdir /user/hadoop/taylor_lyrics
hadoop fs -mkdir /user/hadoop/taylor_lyrics2
hadoop fs -mkdir /user/hadoop/results
```

2. Clone the repository
```
# can also use wget or s3 to download to instance (s3 can upload larger dataset)
git clone https://github.com/612kelly/MapReduce_lyrics.git
```

3. Changed to cloned repository directory
```
cd MapReduce_lyrics
```

4. Check list of files
```
ls taylor_lyrics
ls taylor_lyrics_processed
ls taylor_lyrics_processed2
```

5. Copy the files to HDFS
```
# remove words in brackets
hadoop fs -copyFromLocal taylor_lyrics_processed/* /user/hadoop/taylor_lyrics

# remove stopwords
hadoop fs -copyFromLocal taylor_lyrics_processed2/* /user/hadoop/taylor_lyrics2
```

6. Verify the files are included
```
hadoop fs -ls /user/hadoop/taylor_lyrics
hadoop fs -ls /user/hadoop/taylor_lyrics2
```

7. Run code for **Java** script
```
# Compile the code
javac -classpath $(hadoop classpath) -d . WordCount.java Wordcount_mapper.java Wordcount_reducer.java

# Create JAR file
jar cf wc.jar WordCount*.class Wordcount_mapper*.class Wordcount_reducer*.class

# to delete and rerun result
hadoop fs -rm -r /user/hadoop/results/hadoop_mapreduce

# Perform MapReduce job
time hadoop jar wc.jar WordCount /user/hadoop/taylor_lyrics/* /user/hadoop/results/hadoop_mapreduce

time hadoop jar wc.jar WordCount /user/hadoop/taylor_lyrics2/* /user/hadoop/results/hadoop_mapreduce2

# View the results of the word count from highest to slowest
hadoop fs -cat /user/hadoop/results/hadoop_mapreduce/part-r-00000 | sort -k2,2nr | more
hadoop fs -cat /user/hadoop/results/hadoop_mapreduce2/part-r-00000 | sort -k2,2nr | more
```

8. Run code for **Python** script
```
time hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming*.jar \
-files Wordcount_mapper.py,Wordcount_reducer.py \
-mapper "python3 Wordcount_mapper.py" \
-reducer "python3 Wordcount_reducer.py" \
-input hdfs:///user/hadoop/taylor_lyrics/* \
-output hdfs:///user/hadoop/results/hadoop_mapreduce_py

time hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming*.jar \
-files Wordcount_mapper.py,Wordcount_reducer.py \
-mapper "python3 Wordcount_mapper.py" \
-reducer "python3 Wordcount_reducer.py" \
-input hdfs:///user/hadoop/taylor_lyrics2/* \
-output hdfs:///user/hadoop/results/hadoop_mapreduce_py2

# View the results of the word count from highest to slowest
hadoop fs -cat /user/hadoop/results/hadoop_mapreduce_py/part-00000| sort -k2,2nr | more
hadoop fs -cat /user/hadoop/results/hadoop_mapreduce_py2/part-00000| sort -k2,2nr | more
```

9. Run code for **Spark** script
```
time spark-submit Wordcount_spark.py
time spark-submit Wordcount_spark2.py

# View word count from highest to slowest
hadoop fs -cat /user/hadoop/results/hadoop_mapreduce_spark/part-*| sort -k2,2nr | more
hadoop fs -cat /user/hadoop/results/hadoop_mapreduce_spark2/part-*| sort -k2,2nr | more
```
