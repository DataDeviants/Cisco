from confluent_kafka import Producer
import requests
import json
import time

# Configure your Kafka Producer
p = Producer({'bootstrap.servers': 'localhost:29092',
             'broker.address.family': 'v4'})

for i in range(10):
    data = {'tag ': 'blah',
            'name': 'sam',
            'index': i,
            'score':
            {'row1': 100,
             'row2': 200
             }
            }
    p.produce('orders', json.dumps(data).encode('utf-8'))
    p.flush()
