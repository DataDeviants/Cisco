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

s = requests.Session()
s.headers = {'X-API-Key': apiKey}
# get the floor map via a FloorMapRequest
r = s.get(
    'https://partners.dnaspaces.io/api/partners/v1/maps/5e3d50992e29fe366011d57a87870de9/image')
print(r.status_code)
# md5 to image
md5 = r.headers['Content-MD5']
print(md5)
# save the image
with open('floor.png', 'wb') as f:
    f.write(r.content)