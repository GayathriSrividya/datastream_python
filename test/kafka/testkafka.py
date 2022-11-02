import unittest
import json
import sys
sys.path.append("../..")

from src.kafka.telemetry_class import Telemetry
from datetime import datetime


class TestTelemetry(unittest.TestCase):
    start_time=datetime.now()
    instance=Telemetry('../../data/2021-01-01-1-1609483435390.json.gz')    
    params = json.load(open('../../test/config/kafka_params.json'))

    
    def test_count(self):
        for query, text in self.params['count'].items():
            print(query+"\n")
            self.assertEqual(self.instance.count(), text[0])

    def test_metrics(self):
        for query, text in self.params['metrics'].items():
            print(query+"\n")
            self.assertEqual(self.instance.metrics(text[0]), text[1])


    def test_push(self):
        for query, text in self.params['push'].items():
            print(query+"\n")
            self.assertEqual(self.instance.push(text[0], text[1]), text[2])
    

 