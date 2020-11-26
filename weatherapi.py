import requests
import json
import os
import sys

KEY_FILE = 'weather-api.key'

if not os.path.exists(KEY_FILE):
    print('No API KEY file', file=sys.stderr)
    exit(1)

with open(KEY_FILE) as key_file:
    API_KEY = key_file.read().strip()

URL = rf'https://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID={API_KEY}'
response = requests.get(URL)

response_body = json.loads(response.text)
if response.status_code // 200 == 1:
    print(response_body)
else:
    print('SOMETHING HAS HAPPENED')
    print(response_body['message'])
