from confluent_kafka import Consumer, KafkaException
import pandas as pd
import json

c = Consumer(
    {'bootstrap.servers': 'localhost:29092',
     'broker.address.family': 'v4',
     'auto.offset.reset': 'earliest',
        'group.id': 'mygroup'
     })

c.subscribe(['dnaspaces'])

messages = []

try:
    while True:
        msg = c.poll(1.0)  # timeout set to 1 second

        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        else:
            # Proper message
            print('%% %s [%d] at offset %d with key %s:\n' % (
                msg.topic(), msg.partition(), msg.offset(), str(msg.key())))
            messages.append(json.loads(msg.value().decode('utf-8')))

        if len(messages) > 10:
            break

except KeyboardInterrupt:
    pass
finally:
    c.close()

df = pd.DataFrame(messages)

# make "recordTimestamp" a datetime object
df['recordTimestamp'] = pd.to_datetime(df['recordTimestamp'])

print(df['recordTimestamp']
