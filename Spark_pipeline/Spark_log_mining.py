
import findspark
findspark.init()


import sys
from pyspark.streaming import StreamingContext
from pyspark import SparkContext,SparkConf
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import SparkSession

from Preprocessing import parse_hdfs_file, read_file, dict_label
from Extractor import FeatureExtractor
from Send_email import send_email


import os

if __name__ == "__main__":

    os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars spark-streaming-kafka-0-8-assembly_2.11-2.3.3.jar pyspark-shell' #note that the "pyspark-shell" part is very important!!.

    spark = SparkSession.builder.appName("SSKafka").getOrCreate()



    stream_data = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "test") \
        .option("startingOffsets", "earliest") \
        .load()

    customSchema = StructType([
        StructField("Date", StringType(), True),
        StructField("Time", StringType(), True),
        StructField("Pid", StringType(), True),
        StructField("Level", StringType(), True),
        StructField("Component", StringType(), True),
        StructField("Content", StringType(), True),
        StructField("EventTemplate", StringType(), True),
        StructField("EventId", StringType(), True)
    ])
    label_csv = spark.read.format("csv").option("header", "true").load("anomaly_label.csv")
    APACHE_ACCESS_LOG_PATTERN = '^(\S+) (\S+) (\S+) (\S+) (\S+) (.*)'
    parsed_stream_data = stream_data.rdd.map(lambda df: parse_hdfs_file(df,APACHE_ACCESS_LOG_PATTERN,customSchema))
    read_file_stream = parsed_stream_data.rdd.map(lambda parsed_df: read_file(parsed_df,label_file))
    df_train = spark.createDataFrame(parsed_file,schema = customSchema)
    event_data = read_file_stream.rdd.map(lambda event_df : dict_label(read_file_stream))

    test_mat = data_event['Event Sequence'].values
    featureExtractor = FeatureExtractor()
    x_test = feature_extractor.transform(test_mat)
    prediction = model.predict(x_test)
    model = joblib.load('trained-model.pkl')
    prediction = model.predict(x_test)

    for labels in prediction:

        if label == 1 :
            for event in test_mat:
                event_details = read_file_stream.filter(read_file_stream['EventId'] == event)
                file_name = "event_details"+block_id+".csv"
                event_details.to_csv(file_name, sep=',')
                with open(file_name, 'r') as fp:
                    log_lines = fp.readlines()
                    send_email("!!! Anamoly DETECTED !!!",log_lines )


    sc.stop()
