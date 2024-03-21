from confluent_kafka import Consumer, KafkaException, Producer
import pandas as pd
import json

MY_TENANT_ID = "Simulation-Workspaces"
EVENT_MODE = "DEVICE"

c = Consumer(
    {
        'bootstrap.servers': '10.51.4.43:29092',
        'broker.address.family': 'v4',
        'auto.offset.reset': 'earliest',
        'group.id': 'mygroup'
    }
)

p = Producer({
    'bootstrap.servers': '10.51.4.43:29092',
    'broker.address.family': 'v4'
})

c.subscribe(['dnaspaces'])


def parse_message(msg):
    """
    cols "id,time,floorNumber,x,y,confidence,deviceType"
    """
    event = json.loads(msg.value().decode('utf-8'))
    eventType = event['eventType']
    tenantId = event["partnerTenantId"]
    if eventType == "DEVICE_LOCATION_UPDATE":
        deviceLocationUpdate = event["deviceLocationUpdate"]
        xpos = float(deviceLocationUpdate['xPos'])
        ypos = float(deviceLocationUpdate['yPos'])
        confidence = deviceLocationUpdate['confidenceFactor']
        deviceId = deviceLocationUpdate['device']['deviceId']
        location = deviceLocationUpdate['location']

        # add fields to event
        event["id"] = deviceId
        event["time"] = int(event['recordTimestamp'])
        event["x"] = xpos
        event["y"] = ypos
        event["confidence"] = confidence
        event["deviceType"] = None
        event["deviceInfo"] = None
        event["location"] = location

    elif eventType == "IOT_TELEMETRY":
        iotTelemetry = event["iotTelemetry"]
        detectedPosition = iotTelemetry['detectedPosition']
        xpos = float(detectedPosition['xPos'])
        ypos = float(detectedPosition['yPos'])
        time = int(detectedPosition['lastLocatedTime'])
        confidence = detectedPosition['confidenceFactor']
        deviceInfo = iotTelemetry['deviceInfo']
        deviceType = deviceInfo['deviceType']
        deviceId = deviceInfo['deviceId']
        location = iotTelemetry['location']

        # add fields to event
        event["id"] = deviceId
        event["time"] = time
        event["x"] = xpos
        event["y"] = ypos
        event["confidence"] = confidence
        event["deviceType"] = deviceType
        event["deviceInfo"] = deviceInfo
        event["location"] = location

    return event


try:
    while True:
        msg = c.poll(0.1)  # timeout set to 1 second

        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        else:
            # parse message and add to new topic
            parsed = parse_message(msg)
            # print(parsed)
            # Proper message
            p.produce('dnaspaces_cleaned',
                      key=parsed["eventType"], value=json.dumps(parsed))
            p.flush()


except KeyboardInterrupt:
    pass
finally:
    c.close()
