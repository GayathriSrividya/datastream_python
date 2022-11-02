# required dependencies
from kafka import KafkaConsumer
from json import loads

# pulling events from kafka
consumer = KafkaConsumer('sb-telemetry', bootstrap_servers=['localhost:9092'], group_id='my-group', value_deserializer=lambda x: loads(x.decode('utf-8')), consumer_timeout_ms=100000)

for message in consumer:
   print(message.value)
consumer.close()
 