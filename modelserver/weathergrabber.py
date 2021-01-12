import requests
import os
from datetime import datetime
import json


def get_api_key():
    return os.getenv('API_KEY')


def get_city_id():
    return os.getenv('CITY_ID')


def get_preprocessed_raw_weather_data(raw_data):
    main = raw_data.get('main', {})
    visibility = raw_data.get('visibility', None)
    wind = raw_data.get('wind', {})
    wind_speed = wind.get('speed', None)
    wind_deg = wind.get('deg', None)
    clouds = raw_data.get('clouds', {}).get('all', None)
    sys = raw_data.get('sys', {})
    sunrise = sys.get('sunrise', None)
    sunset = sys.get('sunset', None)
    dt = raw_data.get('dt', None)
    weather = {
        'visibility': visibility,
        'wind_speed': wind_speed,
        'wind_direction_degree': wind_deg,
        'cloudness': clouds,
        'datetime': dt,
        'sunrise': sunrise,
        'sunset': sunset,
        'temp': main.get('temp', None),
        'feels_like': main.get('feels_like', None),
        'pressure': main.get('pressure', None),
        'humidity': main.get('humidity', None)
    }
    
    coord = raw_data.get('coord', None)
    weather_item = raw_data.get('weather', [{}])[0]
    weather_id = weather_item.get('id', None)
    weather_description = weather_item.get('description', None)
    timezone = raw_data.get('timezone', None)
    if not all([weather_id, weather_description, timezone]):
        extra = None
    else:
        extra = {
            'id': weather_id,
            'description': weather_description,
            'timezone': timezone
        }
    
    result = {
        'weather': weather,
        'coord': coord,
        'extra': extra
    }
    return result


def get_processed_weather_data(weather_data):
    weather = weather_data.get('weather', None)
    if not weather:
        return None
    dt = weather.get('datetime', None)
    if not dt:
        return None
    weather['datetime'] = str(datetime.fromtimestamp(dt))
    return weather_data


def save_weather_into_db(data):
    db_dir = os.getenv('WEATHER_DB_PATH')
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    
    weather_date = datetime.fromisoformat(data['weather']['datetime'])
    db_file = os.path.join(db_dir, str(weather_date.date()) + '.json')
    result_data = [data]
    if os.path.exists(db_file):
        with open(db_file) as weather_json:
            existing_data = json.load(weather_json)
            result_data = existing_data + result_data
    with open(db_file, 'w') as weather_json:
        json.dump(result_data, weather_json, indent=3)


api_key = get_api_key()
city_id = get_city_id()

URL = rf'https://api.openweathermap.org/data/2.5/weather?id={city_id}&units=metric&APPID={api_key}'
response = requests.get(URL)

if response.status_code // 200 == 1:
    body = response.json()
    preprocessed_data = get_preprocessed_raw_weather_data(body)
    processed_data = get_processed_weather_data(preprocessed_data)
    save_weather_into_db(processed_data)