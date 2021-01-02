import citylist
from errors import NoSuchCityError, NoWeatherForCity

import os
import json


class ProxyStub:
    def __init__(self, *args):
        city_path = citylist.get_city_list_json_path()
        self._city_list = citylist.get_city_list(city_path)
        self._db = load_weather_db()
    
    def load_available_cities(self):
        cities = self._city_list[:10]
        result = [{
            'id': city.get_city_id(),
            'name': city.get_city_name()
        } for city in cities]
        return result
    
    def load_city_weather(self, city_id):
        filtered = [city for city in self._city_list\
            if city.get_city_id() == city_id]
        if len(filtered) < 1:
            raise NoSuchCityError('No cities with the passed ID')

        city = filtered[0]
        record = self._db.get(city.get_city_id(), None)
        if record is None:
            raise NoWeatherForCity('No weather data for the city')
        weather = record.get('hourly', [])
        return weather


def load_weather_db():
    db_path_env = 'WEATHERDB'
    db_path = os.getenv(db_path_env)
    with open(db_path) as db_file:
        db = json.load(db_file)
        return db


def get_test_city_weather():
    proxy = ProxyStub()
    cities = proxy.load_available_cities()
    city = cities[0]
    weather = proxy.load_city_weather(city['id'])
    return weather


if __name__ == '__main__':
    weather = get_test_city_weather()
    print(weather)