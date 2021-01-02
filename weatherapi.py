import requests
import json
import os
import sys
from datetime import timedelta, datetime

KEY_FILE = 'weather-api.key'

if not os.path.exists(KEY_FILE):
    print('No API KEY file', file=sys.stderr)
    exit(1)

with open(KEY_FILE) as key_file:
    API_KEY = key_file.read().strip()

# URL = rf'https://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID={API_KEY}'
# URL = rf'https://api.openweathermap.org/data/2.5/weather?id=3094802&APPID={API_KEY}'
# URL = rf'https://api.openweathermap.org/data/2.5/onecall?lat=50.083328&lon=19.91667&exclude=minutely&appid={API_KEY}'
# URL = rf'http://history.openweathermap.org/data/2.5/history/city?id=3094802&type=hour&appid={API_KEY}'
stamp = int((datetime.now() - timedelta(days=5)).timestamp())

from client.proxies import citylist

path = citylist.get_city_list_json_path()
cities = citylist.get_city_list(path)[:10]
db = {}
for city in cities:
    lon, lat = city.get_city_lon_lat()
    URL = rf'https://api.openweathermap.org/data/2.5/onecall/timemachine?lon={lon}&lat={lat}&dt={stamp}&appid={API_KEY}'
    response = requests.get(URL)
    if response.status_code // 200 == 1:
        resp_obj = json.loads(response.text)
        hourly = resp_obj['hourly']
        current = resp_obj['current']
        item_to_remove = None
        for item in hourly:
            dt = datetime.fromtimestamp(item['dt'])
            if dt.hour == 0:
                item_to_remove = item
            item['datetime'] = str(dt)
            item['sunrise'] = current['sunrise']
            item['sunset'] = current['sunset']
            del item['weather']
            del item['dt']
            if 'wind_gust' in item:
                del item['wind_gust']
        if item_to_remove is not None:
            hourly.remove(item_to_remove)
        print(city)
        db[city.get_city_id()] = {
            'city': city.asdict(),
            'hourly': hourly
        }
hourly_path = os.getenv('WEATHERDB', None)
if hourly_path is None:
    print('Path in the WEATHERDB var is not set')
else:
    with open('../hourly.json', 'w') as hourly_json:
        json.dump(db, hourly_json, indent=5)
        print('SUCCESS')

# response_body = json.loads(response.text)
# if response.status_code // 200 == 1:
#     print(response_body)
#     with open('../krk-current.json', 'w') as krk_json:
#         json.dump(response_body, krk_json, indent=5)
# else:
#     print('SOMETHING HAS HAPPENED')
#     print(response_body['message'])
