 
import logging
import sys
import os
import json
import jsonschema
from jsonschema import validate
from pyflink.common import  Types, SimpleStringSchema 
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer

# schema validation 
def validate_ds(jsonData):
    validationschema = json.load(open('../../config/metric_schema.json'))
    try:
        validate(instance=jsonData, schema=validationschema)
    except jsonschema.exceptions.ValidationError as err:
        return err
    return True

# converting datastream into json
def update_ds(datastream):
    data=json.dumps((datastream))
    return data

# apply translations on datastream
def transform_ds(datastream):
    data=json.loads(datastream)
    valid=validate_ds(data)
    if (valid==True):
        params={'timestamp': data['timestamp'], 'input_count':data['input_count'], 'time_taken':data['time_taken']}
        metric_data = {}
        for item in data['metrics']:
            metric_data[item['name']] = item['value']
        params.update(metric_data)
        return params
    else:
        print(valid)
        sys.exit()
        

# flink kafka source and sink
def datastream_kafka(env):
    
    deserialization_schema=SimpleStringSchema()

    # flink kafka source to read events from topic sb-telemetry

    consumer = FlinkKafkaConsumer(
        topics='sb-telemetry',
        deserialization_schema=deserialization_schema,
        properties={'bootstrap.servers': 'localhost:9092', 'group.id': 'my-group'}
    )
    consumer.set_start_from_earliest()

    # generating datastream 
    kafka_data = env.add_source(consumer)
    
    # applying transformations on datastream
    kafka_data=kafka_data.map(transform_ds)

    serialization_schema = SimpleStringSchema()
    # Flink kafka sink to push the transformed datastream back to kafka
    producer = FlinkKafkaProducer(
        topic='sb-metrics',
        serialization_schema=serialization_schema,
        producer_config={'bootstrap.servers': 'localhost:9092'})
    print("writing to kafka")
    kafka_data = kafka_data.map(lambda x: update_ds(x),Types.STRING())
    kafka_data.add_sink(producer)
    
    # executing the flink job
    env.execute()
 
if __name__ == '__main__':

    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    # adding jar dependencies
    kafka_jar = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'flink-sql-connector-kafka_2.11-1.14.4.jar')
    env.add_jars("file:///{}".format(kafka_jar))

    print("start reading data from kafka\n")
    datastream_kafka(env)
 