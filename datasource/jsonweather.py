import os
import json


class JsonWeatherData:
    def __init__(self, json_obj={}, json_str=''):
        if not json_obj and not json_str:
            raise ValueError('Must be passed either dict object or JSON string')
        if not isinstance(json_obj, dict):
            raise TypeError('Passed object must be dict')
        if not isinstance(json_str, str):
            raise TypeError('Passed JSON str must be string')

        if json_obj:
            self._data = json_obj
        elif json_str:
            self._data = json.loads(json_str)
    
    def get_today_hourly(self):
        return self._data.get('hourly', [])


def read_weather_json(weather_json_path):
    with open(weather_json_path) as weather_json:
        json_obj = json.load(weather_json)
        return JsonWeatherData(json_obj)


def get_weather_json_path():
    json_path_env = 'WEATHERJSON'
    return os.getenv(json_path_env, None)