import json
import os


class WeatherAPICity:
    """
    Used for proxy stub
    """
    def __init__(self, city_dict):
        self._city_dict = city_dict or {}
    
    def get_city_id(self):
        city = self._city_dict.get('city', {})
        city_id = city.get('id', {})
        id_value = city_id.get('$numberLong', None)
        return id_value
    
    def get_city_lon_lat(self):
        city = self._city_dict.get('city', {})
        coord = city.get('coord', {})
        lon = coord.get('lon', None)
        lat = coord.get('lat', None)
        return lon, lat
    
    def get_city_name(self):
        city = self._city_dict.get('city', {})
        name = city.get('name', None)
        return name
    
    def get_city_searchname(self):
        city = self._city_dict.get('city', {})
        name = city.get('findname', None)
        return name
    
    def asdict(self):
        lon, lat = self.get_city_lon_lat()
        return {
            'id': self.get_city_id(),
            'name': self.get_city_name(),
            'lon': lon,
            'lat': lat
        }
    
    def __str__(self):
        return f'{self.get_city_name()} : {self.get_city_id()}'


def get_city_list(city_list_json_path):
    with open(city_list_json_path) as citylist_json:
        raw_cities = json.load(citylist_json)
        cities = [WeatherAPICity(raw_city) for raw_city in raw_cities]
        return cities


def get_city_list_json_path():
    CITYLIST_ENV = 'WEATHERAPICITIES'
    return os.getenv(CITYLIST_ENV)
