from confluent_kafka import Consumer, KafkaException
import pandas as pd
import json


c = Consumer(
    {
        'bootstrap.servers': '10.51.4.43:29092',
        'broker.address.family': 'v4',
        'auto.offset.reset': 'earliest',
        'group.id': 'mygroup'
    }
)

c.subscribe(['dnaspaces_cleaned'])

messages = []

try:
    while True:
        msg = c.poll(0.1)  # timeout set to 1 second

        if msg is None:
            print("None")
            continue
        if msg.error():
            raise KafkaException(msg.error())
        else:
            # Proper message
            print(json.loads(msg.value().decode('utf-8')))

        if len(messages) > 10:
            break

except KeyboardInterrupt:
    pass
finally:
    c.close()


