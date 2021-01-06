import urllib.parse as urlparse
from urllib.error import URLError


def url_valid(url):
    parse_res = urlparse.urlparse(url)
    if not parse_res.scheme or not parse_res.netloc:
        return False
    return True


def get_key_storage_proxy():
    return KeyStorageProxy('localhost:6379')


class KeyStorageProxy:
    def __init__(self, storage_address):
        self._storage_address = storage_address
    
    def get_available_model_servers(self):
        return [{
            'id': 755889,
            'name': 'Wieliczka'
        }]
    
    def get_model_server_address(self, server_id):
        return 'http://localhost:7722'


class ModelProxy:
    def __init__(self, model_address):
        if not url_valid(model_address):
            raise URLError('Invalid model server address')

        self._model_address = model_address
    
    def get_city_weather(self):
        return TEMP_HOURLY_WEATHER_DATA


TEMP_HOURLY_WEATHER_DATA = [
               {
                    "temp": 275.23,
                    "feels_like": 269.9,
                    "pressure": 999,
                    "humidity": 66,
                    "dew_point": 269.96,
                    "clouds": 0,
                    "visibility": 10000,
                    "wind_speed": 4.1,
                    "wind_deg": 40,
                    "datetime": "2020-12-28 01:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 275.15,
                    "feels_like": 269.82,
                    "pressure": 998,
                    "humidity": 66,
                    "dew_point": 269.9,
                    "clouds": 20,
                    "visibility": 10000,
                    "wind_speed": 4.1,
                    "wind_deg": 60,
                    "datetime": "2020-12-28 02:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 275.42,
                    "feels_like": 270.94,
                    "pressure": 996,
                    "humidity": 86,
                    "dew_point": 273.32,
                    "clouds": 0,
                    "visibility": 10000,
                    "wind_speed": 3.6,
                    "wind_deg": 40,
                    "datetime": "2020-12-28 03:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 274.5,
                    "feels_like": 270.72,
                    "pressure": 991,
                    "humidity": 92,
                    "dew_point": 273.35,
                    "clouds": 0,
                    "visibility": 10000,
                    "wind_speed": 2.6,
                    "wind_deg": 50,
                    "datetime": "2020-12-28 04:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 274.91,
                    "feels_like": 270.14,
                    "pressure": 990,
                    "humidity": 92,
                    "dew_point": 273.75,
                    "clouds": 0,
                    "visibility": 10000,
                    "wind_speed": 4.1,
                    "wind_deg": 60,
                    "datetime": "2020-12-28 05:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 275.49,
                    "feels_like": 270.88,
                    "pressure": 989,
                    "humidity": 80,
                    "dew_point": 272.49,
                    "clouds": 0,
                    "visibility": 10000,
                    "wind_speed": 3.6,
                    "wind_deg": 20,
                    "datetime": "2020-12-28 06:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 276.51,
                    "feels_like": 270.98,
                    "pressure": 991,
                    "humidity": 66,
                    "dew_point": 271.05,
                    "clouds": 0,
                    "visibility": 10000,
                    "wind_speed": 4.6,
                    "wind_deg": 20,
                    "datetime": "2020-12-28 07:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 276.4,
                    "feels_like": 271.91,
                    "pressure": 988,
                    "humidity": 66,
                    "dew_point": 270.95,
                    "clouds": 0,
                    "visibility": 10000,
                    "wind_speed": 3.1,
                    "wind_deg": 350,
                    "datetime": "2020-12-28 08:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 276.89,
                    "feels_like": 271.76,
                    "pressure": 987,
                    "humidity": 66,
                    "dew_point": 271.37,
                    "clouds": 0,
                    "visibility": 10000,
                    "wind_speed": 4.1,
                    "wind_deg": 40,
                    "datetime": "2020-12-28 09:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 278.9,
                    "feels_like": 276.27,
                    "pressure": 987,
                    "humidity": 80,
                    "dew_point": 275.72,
                    "clouds": 20,
                    "visibility": 10000,
                    "wind_speed": 1.5,
                    "wind_deg": 70,
                    "datetime": "2020-12-28 10:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 279.72,
                    "feels_like": 273.62,
                    "pressure": 988,
                    "humidity": 70,
                    "dew_point": 274.65,
                    "clouds": 20,
                    "visibility": 10000,
                    "wind_speed": 6.2,
                    "wind_deg": 80,
                    "datetime": "2020-12-28 11:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 279.8,
                    "feels_like": 276.59,
                    "pressure": 989,
                    "humidity": 70,
                    "dew_point": 274.72,
                    "clouds": 20,
                    "visibility": 10000,
                    "wind_speed": 2.1,
                    "wind_deg": 40,
                    "datetime": "2020-12-28 12:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 279.65,
                    "feels_like": 276.41,
                    "pressure": 990,
                    "humidity": 70,
                    "dew_point": 274.58,
                    "clouds": 20,
                    "visibility": 10000,
                    "wind_speed": 2.1,
                    "wind_deg": 180,
                    "datetime": "2020-12-28 13:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 279.37,
                    "feels_like": 276.03,
                    "pressure": 990,
                    "humidity": 68,
                    "dew_point": 273.91,
                    "clouds": 20,
                    "visibility": 10000,
                    "wind_speed": 2.1,
                    "wind_deg": 230,
                    "datetime": "2020-12-28 14:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 278.72,
                    "feels_like": 274.58,
                    "pressure": 993,
                    "humidity": 56,
                    "dew_point": 270.93,
                    "clouds": 40,
                    "visibility": 10000,
                    "wind_speed": 2.6,
                    "wind_deg": 90,
                    "datetime": "2020-12-28 15:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 278.6,
                    "feels_like": 275.33,
                    "pressure": 993,
                    "humidity": 60,
                    "dew_point": 271.66,
                    "clouds": 20,
                    "visibility": 10000,
                    "wind_speed": 1.5,
                    "wind_deg": 150,
                    "datetime": "2020-12-28 16:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 278.39,
                    "feels_like": 273.51,
                    "pressure": 991,
                    "humidity": 56,
                    "dew_point": 270.66,
                    "clouds": 20,
                    "visibility": 10000,
                    "wind_speed": 3.6,
                    "wind_deg": 130,
                    "datetime": "2020-12-28 17:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 277.72,
                    "feels_like": 273.35,
                    "pressure": 989,
                    "humidity": 52,
                    "dew_point": 269.23,
                    "clouds": 20,
                    "visibility": 10000,
                    "wind_speed": 2.6,
                    "wind_deg": 160,
                    "datetime": "2020-12-28 18:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 277.94,
                    "feels_like": 272.33,
                    "pressure": 991,
                    "humidity": 69,
                    "dew_point": 272.79,
                    "clouds": 0,
                    "visibility": 10000,
                    "wind_speed": 5.1,
                    "wind_deg": 70,
                    "datetime": "2020-12-28 19:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 277.89,
                    "feels_like": 273.32,
                    "pressure": 988,
                    "humidity": 69,
                    "dew_point": 272.75,
                    "clouds": 0,
                    "visibility": 10000,
                    "wind_speed": 3.6,
                    "wind_deg": 60,
                    "datetime": "2020-12-28 20:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 277.46,
                    "feels_like": 273.32,
                    "pressure": 986,
                    "humidity": 74,
                    "dew_point": 273.24,
                    "clouds": 0,
                    "visibility": 10000,
                    "wind_speed": 3.1,
                    "wind_deg": 50,
                    "datetime": "2020-12-28 21:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 278.12,
                    "feels_like": 274.27,
                    "pressure": 990,
                    "humidity": 81,
                    "dew_point": 275.14,
                    "clouds": 0,
                    "visibility": 10000,
                    "wind_speed": 3.1,
                    "wind_deg": 50,
                    "datetime": "2020-12-28 22:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               },
               {
                    "temp": 277.89,
                    "feels_like": 274.36,
                    "pressure": 985,
                    "humidity": 81,
                    "dew_point": 274.91,
                    "clouds": 0,
                    "visibility": 10000,
                    "wind_speed": 2.6,
                    "wind_deg": 60,
                    "datetime": "2020-12-28 23:00:00",
                    "sunrise": 1609137483,
                    "sunset": 1609166675
               }
          ]