from telemetry_class import Telemetry
import json
from datetime import datetime
from json import dumps
keys=[]
results=[]
summary_list=[]
start_time=datetime.now()

# creating instance for class Telemetry

instance=Telemetry('../../data/2021-01-01-1-1609483435390.json.gz')

# querying on data --> generating summaries

inputs=instance.count()

metric_data=json.load(open("../../config/metric_params.json"))


for query, txt in metric_data.items():
    keys.append(query)
    results.append(instance.metrics(txt))


time_taken=(datetime.now()-start_time).seconds/1000

# creating a json file

for index in range (len(keys)):
    summary_list.append({"name":keys[index], "value":results[index]})

filters= {"timestamp": (datetime.now().timestamp())*1000, "input_count": inputs, "time_taken": time_taken, "metrics": summary_list}

metrics=json.dumps(filters, indent=len(filters))
print(metrics)

# pushing events into kafka
# Make sure that the Kafka cluster is started

instance.push(metrics, 'sb-telemetry')