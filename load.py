import requests
import json
import socket
import os
import sys

def get_API_Key_and_auth():
  # Gets public key from spaces and places in correct format
  print("-- No API Key Found --")

  # Gets user to paste in generated token from app
  token = input('Enter provided API key here: ')

  # Writes activation key to file. This key can be used to open up Firehose connection
  f = open("API_KEY.txt", "a")
  f.write(token)
  f.close()
  return token


# work around to get IP address on hosts with non resolvable hostnames
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP_ADRRESS = s.getsockname()[0]
s.close()
url = 'http://' + str(IP_ADRRESS) + '/update/'

# Tests to see if we already have an API Key
try:
  if os.stat("API_KEY.txt").st_size > 0:
    # If we do, lets use it
    f = open("API_KEY.txt")
    apiKey = f.read()
    f.close()
  else:
    # If not, lets get user to create one
    apiKey = get_API_Key_and_auth()
except:
  apiKey = get_API_Key_and_auth()


# Opens a new HTTP session that we can use to terminate firehose onto
s = requests.Session()
s.headers = {'X-API-Key': apiKey}
r = s.get(
    'https://partners.dnaspaces.io/api/partners/v1/firehose/events', stream=True
  )  # Change this to .io if needed


jsonfile = open("logs.json", 'r+')
# jsonfile.truncate(0)

posfile = open("pos.csv", 'r+')
posfile.truncate(0)

posfile.write("id,time,floorNumber,x,y,confidence,deviceType\n")

myTenantId = "Simulation-Workspaces"

event_mode = "DEVICE"

# Jumps through every new event we have through firehose
print("Starting Stream")
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
      # print(location['inferredLocationTypes'][0])
      if location['inferredLocationTypes'][0] == "NETWORK":
        continue
      while True:
        if "floorNumber" in location.keys():
          floorNumber = location['floorNumber']
          break
        else:
          location = location['parent']
      if deviceId == "device-Gld2dbQFYnTDDzxTJYuP4":
        print(f"{deviceId},{time},{floorNumber},{xpos},{ypos},{confidence}")
        print(location['inferredLocationTypes'])
      posfile.write(f"{deviceId},{time},{floorNumber},{xpos},{ypos},{confidence}\n")
    except Exception as e:
      print("Error: " + str(e))


