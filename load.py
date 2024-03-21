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
jsonfile.truncate(0)

posfile = open("pos.csv", 'r+')
posfile.truncate(0)

posfile.write("id,x,y\n")

# Jumps through every new event we have through firehose
print("Starting Stream")
for line in r.iter_lines():
  if line:
    # decodes payload into useable format
    decoded_line = line.decode('utf-8')
    event = json.loads(decoded_line)

    eventType = event['eventType']
    tenantId = event["partnerTenantId"]
    #print(eventType)

    # writes whole json
    #jsonfile.write(str(json.dumps(event, indent=2, sort_keys=True)))

    if eventType == "IOT_TELEMETRY" and tenantId == "Simulation-Workspaces":
      try:
        xpos = float(event['iotTelemetry']['detectedPosition']['xPos'])
        ypos = float(event['iotTelemetry']['detectedPosition']['yPos'])
        time = event['iotTelemetry']['detectedPosition']['lastLocatedTime']
        deviceId = event['iotTelemetry']['deviceInfo']['deviceId']
        posfile.write(f"{deviceId},{time},{xpos},{ypos}\n")
      except KeyError as e:
        print(e)

