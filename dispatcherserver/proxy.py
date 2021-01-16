import urllib.parse as urlparse
import os
import requests
from http import HTTPStatus
from urllib.error import URLError
from redis import Redis
from datetime import date

from errors import ModelServerException, InvalidInputException


def url_valid(url):
    parse_res = urlparse.urlparse(url)
    if not parse_res.scheme or not parse_res.netloc:
        return False
    return True


STORAGE_HOST_ENV = 'STORAGE_HOST'
STORAGE_PORT_ENV = 'STORAGE_PORT'
def get_key_storage_proxy():
    storage_host = os.getenv(STORAGE_HOST_ENV, 'localhost')
    storage_port = os.getenv(STORAGE_PORT_ENV, '6379')
    return KeyStorageProxy(storage_host, int(storage_port))


class KeyStorageProxy:
    def __init__(self, storage_host, storage_port):
        self._redis = Redis(storage_host, storage_port, decode_responses=True)
    
    def get_available_model_servers(self):
        servers = self._redis.keys('city_*')
        result = []
        for server_id in servers:
            if self._redis.type(server_id) != 'hash':
                continue

            name, server_id = self._redis.hmget(server_id, 'name', 'id')
            result.append({
                'id': server_id,
                'name': name
            })
        return result
    
    def get_model_server_address(self, server_id):
        server_url = self._redis.hget(f'city_{server_id}', 'url')
        return server_url


class ModelProxy:
    def __init__(self, model_address):
        if not url_valid(model_address):
            raise URLError('Invalid model server address')

        self._model_address = model_address
    
    def get_city_current_weather(self):
        url = urlparse.urljoin(self._model_address, '/weather/current')
        response = requests.get(url)
        if response.status_code // 500 == 1:
            raise ModelServerException( \
                'Internal error on the upstream server', \
                HTTPStatus.BAD_GATEWAY)
        elif response.status_code // 400 == 1:
            raise Exception('This server sends wrong data')
        result = response.json()
        return result
    
    def get_city_weather(self, start_date=date.today(), end_date=date.today()):
        url = urlparse.urljoin(self._model_address, '/weather/history')
        query_params = {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
        response = requests.get(url, params=query_params)
        if response.status_code // 500 == 1:
            raise ModelServerException( \
                'Internal error on the upstream server', \
                HTTPStatus.BAD_GATEWAY)
        elif response.status_code // 400 == 1:
            response_msg = response.json().get('message', 'Invalid input data')
            raise InvalidInputException(response_msg, response.status_code)
        result = response.json()
        return result
