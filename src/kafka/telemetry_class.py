from kafka import KafkaProducer
import json
from json import dumps
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode

class Telemetry:

    # building spark session
    
    spark=SparkSession.builder.appName("push-to-kafka").config('spark.sql.debug.maxToStringFields', 1000).getOrCreate()

    def __init__(self, file_path):
        self.file_path=file_path
        self.telemetry=self.spark.read.json(self.file_path, encoding='utf-8')
   
    def count(self):
         
        return self.telemetry.select('*').count()
         
    def metrics(self, query):
        try:
            exec("self.result={}".format(query))
            return self.result
        except:
            print("invalid input!!")
            return -1
   
    def push(self, metrics, topic):
        
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: x.encode('utf-8'))
        producer.send('{}'.format(topic), metrics)
        print("events pushed into kafka successfully")
    