import requests
import json

with open("SF_KEY.txt") as f:
  apiKey = f.read()

map_ids = ['a06add6866a28b3ce9ca6f5de19692d9']

s = requests.Session()
s.headers = {"X-API-Key": apiKey, "partnerTenantId": "F7EE24937F9244518E0CBEDEA3BEB05F"}

for j, id in enumerate(map_ids):
  r = s.get("https://partners.dnaspaces.io/api/partners/v1/maps/" + id + "/image")
  print(r.status_code)
  md5 = r.headers["Content-MD5"]
  with open("res/floor" + str(j+1) + ".png", "wb") as f:
    f.write(r.content)

    u = s.get("https://partners.dnaspaces.io/api/partners/v1/maps/" + id)
    print(u.status_code)
    with open("res/floor" + str(j+1) + ".json", "w") as f:
      f.write(json.dumps(u.json(), indent=4))