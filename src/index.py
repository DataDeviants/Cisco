import requests
import json


apiKeyFile = open("SF_KEY.txt")
apiKey = apiKeyFile.read()
s = requests.Session()
s.headers = {"X-API-Key": apiKey}
r = s.get("https://partners.dnaspaces.io/api/partners/v1/firehose/events", stream=True)

jsonfile = open("res/logs.json", 'w+')

for line in r.iter_lines():
    if line:
        decoded_line = line.decode("utf-8")
        jsonfile.write(decoded_line + "\n")
        event = json.loads(decoded_line)
        eventType = event["eventType"]
        if eventType != "IOT_TELEMETRY":
            print(eventType)
        tenantId = event["partnerTenantId"]
        if tenantId != myTenantId:
            continue
        if eventType == "DEVICE_LOCATION_UPDATE":
            deviceLocationUpdate = event["deviceLocationUpdate"]
            xpos = float(deviceLocationUpdate["xPos"])
            ypos = float(deviceLocationUpdate["yPos"])
            time = int(event["recordTimestamp"])
            confidence = deviceLocationUpdate["confidenceFactor"]
            try:
                deviceId = deviceLocationUpdate["device"]["deviceMacAddress"]
            except:
                try:
                    deviceId = deviceLocationUpdate["device"]["macAddress"]
                except:
                    raise Exception("No device id")
            if unset:
                myDeviceId = deviceId
                unset = False
            if not unset and deviceId != myDeviceId:
                continue
            location = deviceLocationUpdate["location"]
            with open("res/pos.csv", "a") as posfile:
              posfile.write(f"{xpos},{ypos}\n")
            print(f"Device {deviceId} at {xpos}, {ypos}")
