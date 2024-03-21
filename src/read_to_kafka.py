from confluent_kafka import Producer
import requests
import json
import time

# Configure your Kafka Producer
p = Producer({'bootstrap.servers': 'localhost:29092',
             'broker.address.family': 'v4'})

s = requests.Session()
s.headers.update({'X-API-Key': "A957EA09EC954A378BDDA857095A1040"})


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
        # Publish data to Kafka as strings
        p.produce('test', json.dumps(data).encode('utf-8'))
        p.flush()
    time.sleep(0.5)  # Wait before fetching more data
