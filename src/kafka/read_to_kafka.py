from confluent_kafka import Producer
import requests
import json
import time

# Configure your Kafka Producer
p = Producer({'bootstrap.servers': '10.51.4.43:29092',
             'broker.address.family': 'v4'})

s = requests.Session()
s.headers.update({'X-API-Key': "E40232AE3A3D4096A1586BB944296CEC"})


def fetch_data():
    r = s.get(
        'https://partners.dnaspaces.io/api/partners/v1/firehose/events', stream=True)
    # Iterate over lines as they are streamed
    for line in r.iter_lines():
        if line:  # Filter out keep-alive new lines
            json_line = json.loads(line)
            yield json_line


while True:
    data_stream = fetch_data()
    for data in data_stream:  # Loop over the generator
        # Publish data to Kafka as json
        p.produce('dnaspaces', key='event', value=json.dumps(data))
        p.flush()
    time.sleep(0.5)  # Wait before fetching more data
