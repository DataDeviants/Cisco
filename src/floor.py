import requests
import json
import socket
import os
with open("API_KEY.txt") as f:
  apiKey = f.read()

map_ids = ['a06add6866a28b3ce9ca6f5de19692d9', '5e3d50992e29fe366011d57a87870de9']

s = requests.Session()
s.headers = {"X-API-Key": apiKey, "partnerTenantId": "Simulation-Workspaces"}

for j, id in enumerate(map_ids):
  r = s.get("https://partners.dnaspaces.io/api/partners/v1/maps/" + id + "/image")
  print(r.status_code)
  md5 = r.headers["Content-MD5"]
  with open("floor" + str(j+1) + ".png", "wb") as f:
    f.write(r.content)

    u = s.get("https://partners.dnaspaces.io/api/partners/v1/maps/" + id)
    print(u.status_code)
    with open("floor" + str(j+1) + ".json", "w") as f:
      f.write(json.dumps(u.json(), indent=4))