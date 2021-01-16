import os
import json
from datetime import date


def get_json_db_adapter():
    db_path = os.getenv('WEATHER_DB_PATH')
    return JsonWeatherDbAdapter(db_path)


class JsonWeatherDbAdapter:
    def __init__(self, dbpath):
        if not dbpath or not os.path.exists(dbpath):
            raise ValueError('No DB by this path')
        self._dbpath = dbpath
    
    def get_current_weather(self):
        list_cmd = f'ls -t -1 {self._dbpath} | head -1'
        with os.popen(list_cmd) as pipe:
            latest_date_weather_path = list(pipe)[0].strip()
        weather_path = os.path.join(self._dbpath, latest_date_weather_path)
        with open(weather_path) as latest_weather_data_json:
            data = json.load(latest_weather_data_json)
            return data[-1] if len(data) > 0 else []
    
    def get_weather_for_period(self, start_date, end_date):
        if start_date > end_date:
            raise ValueError('Incorrect date range')

        result = []
        for weather_json_name in os.listdir(self._dbpath):
            date_part = os.path.splitext(weather_json_name)[0]
            json_date = date.fromisoformat(date_part)
            if start_date <= json_date <= end_date:
                json_path = os.path.join(self._dbpath, weather_json_name)
                with open(json_path) as weather_json:
                    data = json.load(weather_json)
                    for entry in data:
                        result.append(entry['weather'])
        return result
