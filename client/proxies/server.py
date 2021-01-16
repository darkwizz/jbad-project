from client.errors import ServerError, BadInputError, \
    ServerUnavailableError, ConfigurationError

import requests
import urllib.parse as urlparse
from http import HTTPStatus


class ServerProxy:
    def __init__(self, server_address, scheme='http'):
        if scheme not in ('http', 'https'):
            raise ConfigurationError('Incorrect HTTP scheme provided')

        server_url = urlparse.urlunparse((scheme, server_address, '/', '', '', ''))
        response = requests.get(server_url)
        if response.status_code != HTTPStatus.NO_CONTENT:
            raise ServerUnavailableError('Server is not available. Provide a correct address or try later')

        self._server_address = server_address
        self._scheme = scheme
    
    def _get_request_response_data(self, path, **query_args):
        cities_url = urlparse.urlunparse((self._scheme, \
            self._server_address, path, '', '', ''))
        response = requests.get(cities_url, params=query_args)
        response_body = response.json()
        if response.status_code // 500 == 1:
            message = response_body.get('message', \
                f'Server Error {response.status_code}')
            raise ServerError(message)
        if response.status_code // 400 == 1:
            message = response_body.get('message')
            raise BadInputError(message)
        return response_body
    
    def load_available_cities(self):
        return self._get_request_response_data('cities')
    
    def load_city_current_weather(self, city_id):
        path = f'cities/{urlparse.quote(str(city_id))}/weather/current'
        return self._get_request_response_data(path)
    
    def load_city_weather(self, city_id, start_date, end_date):
        path = f'cities/{urlparse.quote(str(city_id))}/weather'
        return self._get_request_response_data(path, start_date=start_date, end_date=end_date)
