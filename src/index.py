import requests


apiKeyFile = open("SF_KEY.txt")
apiKey = apiKeyFile.read()
s = requests.Session()
s.headers = {'X-API-Key': apiKey}
r = s.get('https://partners.dnaspaces.io/api/partners/v1/firehose/events', stream=True)

jsonfile = open("res/logs.json", 'w+')

for line in r.iter_lines():
  if line:
    decoded_line = line.decode('utf-8')
    jsonfile.write(decoded_line + "\n")