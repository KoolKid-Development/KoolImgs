import requests
import json
response_API = requests.get('https://kool-kid.xyz/koolimgs/info.json')
data = response_API.text
getjson = json.loads(data)
versiondata = getjson['KoolIMGS']['Version']