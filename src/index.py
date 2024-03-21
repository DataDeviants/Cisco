import requests
import json
import datetime

apiKeyFile = open("OLD_KEY.txt")
apiKey = apiKeyFile.read()
s = requests.Session()
s.headers = {"X-API-Key": apiKey}
r = s.get("https://partners.dnaspaces.io/api/partners/v1/firehose/events", stream=True)

jsonfile = open("res/logs.json", 'w+')

myTenantId = "Simulation-Workspaces"

unset = True

for line in r.iter_lines():
    if line:
        decoded_line = line.decode("utf-8")
        jsonfile.write(decoded_line + "\n")
        event = json.loads(decoded_line)
        eventType = event["eventType"]
        tenantId = event["partnerTenantId"]
        if tenantId != myTenantId:
            continue
        time = int(event["recordTimestamp"])
        print(eventType, time)
        # time from unix to human readable
        real_time = datetime.datetime.fromtimestamp(time/1000).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Time: {real_time}")
        if eventType != "IOT_TELEMETRY":
            print(eventType)
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
