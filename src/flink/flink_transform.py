 
import logging
import sys
import os
import json
from pyflink.common import  Types, SimpleStringSchema 
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
 
def update_ds(datastream):
    data=json.dumps((datastream))
    return data
def transform_ds(datastream):
    data=json.loads(datastream)
    metrics_name=[]
    measure=[]
    params={'timestamp':'{}'.format(data["timestamp"]), 'input_count':'{}'.format(data['input_count']), 'time_taken':'{}'.format(data['time_taken'])}
    for i in range(len(data['metrics'])):
        metrics_name.append(data["metrics"][i]['name'])
        measure.append(data['metrics'][i]['value'])
    metric_data={metrics_name[i]: measure[i] for i in range(len(metrics_name))}
    params.update(metric_data)
    return params
  
def datastream_kafka(env):
    deserialization_schema=SimpleStringSchema()
    consumer = FlinkKafkaConsumer(
        topics='sb-telemetry',
        deserialization_schema=deserialization_schema,
        properties={'bootstrap.servers': 'localhost:9092', 'group.id': 'my-group', 'consumer.timeout':'10'}
    )
     
    consumer.set_start_from_earliest()
    kafka_data = env.add_source(consumer)
    kafka_data=kafka_data.map(transform_ds)
    serialization_schema = SimpleStringSchema()
    producer = FlinkKafkaProducer(
        topic='sb-metrics',
        serialization_schema=serialization_schema,
        producer_config={'bootstrap.servers': 'localhost:9092'})
    print("writing to kafka")
    kafka_data = kafka_data.map(lambda x: update_ds(x),Types.STRING())
    kafka_data.add_sink(producer)
    
    env.execute()
 
if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    kafka_jar = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'flink-sql-connector-kafka_2.11-1.14.4.jar')
    env.add_jars("file:///{}".format(kafka_jar))

    print("start reading data from kafka\n")
    datastream_kafka(env)
 