import json

jsonfile = open("res/logs.json", 'r+')

posfile = open("res/pos.csv", 'r+')
posfile.truncate(0)

# write csv header
posfile.write("id,time,floorNumber,x,y,confidence,deviceType\n")

myTenantId = "Simulation-Workspaces"
event_mode = "DEVICE"

for line in jsonfile.readlines():
  if line:
    try:
      event = json.loads(line)

      jsonfile.write(str(json.dumps(event, indent=2, sort_keys=True)))

      eventType = event['eventType']
      tenantId = event["partnerTenantId"]
      if tenantId != myTenantId:
        continue
      if eventType == "DEVICE_LOCATION_UPDATE" and event_mode == "DEVICE":
        deviceLocationUpdate = event["deviceLocationUpdate"]
        xpos = float(deviceLocationUpdate['xPos'])
        ypos = float(deviceLocationUpdate['yPos'])
        time = int(event['recordTimestamp'])
        confidence = deviceLocationUpdate['confidenceFactor']

        deviceId = deviceLocationUpdate['device']['deviceId']

        location = deviceLocationUpdate['location']
        
      elif eventType == "IOT_TELEMETRY" and event_mode == "IOT":
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
      else:
        if eventType != "DEVICE_LOCATION_UPDATE" and eventType != "IOT_TELEMETRY":
          print(eventType)
        continue

      floorNumber = None
      while True:
        if "floorNumber" in location.keys():
          floorNumber = location['floorNumber']
          break
        else:
          location = location['parent']
          
      posfile.write(f"{deviceId},{time},{floorNumber},{xpos},{ypos},{confidence}\n")
    except Exception as e:
      print("Error: " + str(e))


