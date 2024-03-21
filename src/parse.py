import json

jsonfile = open("res/logs.json", 'r+')

posfile = open("res/pos.csv", 'w+')
posfile.truncate(0)

# write csv header
posfile.write("id,time,floorNumber,x,y,confidence,deviceType\n")

myTenantId = "F7EE24937F9244518E0CBEDEA3BEB05F"
event_mode = "IOT"

for line in jsonfile.readlines():
  if line:
    try:
      event = json.loads(line)

      eventType = event['eventType']
      tenantId = event["partnerTenantId"]
      if tenantId != myTenantId:
        print("Not my tenant")
        continue
      
      if eventType == "DEVICE_LOCATION_UPDATE" and event_mode == "DEVICE":
        deviceLocationUpdate = event["deviceLocationUpdate"]
        xpos = float(deviceLocationUpdate['xPos'])
        ypos = float(deviceLocationUpdate['yPos'])
        time = int(event['recordTimestamp'])
        confidence = deviceLocationUpdate['confidenceFactor']

        deviceId = deviceLocationUpdate['device']['deviceMacAddress']

        location = deviceLocationUpdate['location']
        
      elif eventType == "IOT_TELEMETRY" and event_mode == "IOT":
        iotTelemetry = event["iotTelemetry"]
        if "detectedPosition" not in iotTelemetry.keys():
          continue
        detectedPosition = iotTelemetry['detectedPosition']
        xpos = float(detectedPosition['xPos'])
        ypos = float(detectedPosition['yPos'])
        time = int(detectedPosition['lastLocatedTime'])
        confidence = detectedPosition['confidenceFactor']

        deviceInfo = iotTelemetry['deviceInfo']
        deviceType = deviceInfo['deviceType']
        deviceId = deviceInfo['deviceMacAddress']

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


