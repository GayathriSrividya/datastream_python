from kafka import KafkaProducer
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode

class Telemetry:

    ''' 
        Description of class Telemetry
        
        This is a class to read telemetry data using pyspark, query on the data and push the results into kafka.

        Attributes:
        ----------
        spark dataframe named telemetry contains telemetry specifications

        Methods defined here:
        ---------------------
        count(self)
            output: number of rows in the dataframe

        metrics(self, query)
            input: query, contains pyspark sql query to be executed
            output: results of the executed query

        push(self, metrics, topic)
            input: data to be pushed into kafka
            output: name of the kafka topic

    '''
    
    spark=SparkSession.builder.appName("push-to-kafka").config('spark.sql.debug.maxToStringFields', 1000).getOrCreate()

    def __init__(self, file_path):
        '''

            Default Constructor for Telemetry
            Parameters:
            ----------
            self, telemetry

        '''
        self.file_path=file_path
        self.telemetry=self.spark.read.json(self.file_path, encoding='utf-8')
   
    def count(self):
        '''
            Summary Line
            Extended description of count(self)

            parameters:
            -----------
            self
            returns the number of rows in Dataframe
        '''
        return self.telemetry.select('*').count()
        
    def metrics(self, query):
        '''
            Summary Line 
            Extended Description of metrics(self, query)

            parameters:
            ----------
            self, query 

            executes pyspark sql query
            returns the results of query execution
            raises exception if any

        '''
        try:
            exec("self.result={}".format(query))
            return self.result
        except:
            print("invalid input!!")
            return -1
   
    def push(self, metrics, topic):
        '''
            Summary Line
            Extended Description of push(self, metrics, topic)

            parameters:
            -----------
            self, metrics, topics 

            invokes KafkaProducer class with necessary configurations
            encodes the data present metrics
            sends encoded in metrics to kafka as events
            prints the status 
        '''
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: x.encode('utf-8'))
        producer.send('{}'.format(topic), metrics)
        print("events pushed into kafka successfully")
    