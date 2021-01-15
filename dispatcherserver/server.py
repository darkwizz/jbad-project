from errors import ModelServerException

from flask import Flask, jsonify
from http import HTTPStatus
from urllib.error import URLError


app = Flask(__name__)


def get_model_server_proxy(server_id):
    from proxy import ModelProxy, get_key_storage_proxy

    storage_proxy = get_key_storage_proxy()
    model_address = storage_proxy.get_model_server_address(server_id)
    app.logger.debug(f'Stored address for {server_id}: {model_address}')
    model_proxy = ModelProxy(model_address)
    return model_proxy


@app.route('/')
def ping():
    return '', HTTPStatus.NO_CONTENT


@app.route('/cities/')
def get_available_cities():
    from proxy import get_key_storage_proxy

    storage_proxy = get_key_storage_proxy()
    cities = storage_proxy.get_available_model_servers()
    return jsonify(cities)


@app.route('/cities/<int:city_id>/weather/current')
def get_city_current_weather(city_id):
    try:
        model_proxy = get_model_server_proxy(city_id)
        result = model_proxy.get_city_current_weather()
        return jsonify(result)
    except URLError as err:
        app.logger.error(f'Error for city {city_id} - {err.reason}')
        return {'message': err.reason}, HTTPStatus.INTERNAL_SERVER_ERROR
    except ModelServerException as ex:
        app.logger.error(f'Error for city {city_id} - {ex.message}')
        return {'message': ex.message}, ex.http_code
    except Exception as ex:
        app.logger.error(f'Internal error for city {city_id} - {ex.with_traceback()}')
        return {'message': 'Internal server error'}, HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/cities/<int:city_id>/weather')
def get_city_weather(city_id):
    try:
        model_proxy = get_model_server_proxy(city_id)
        return jsonify(model_proxy.get_city_weather())
    except URLError as err:
        app.logger.error(f'Error for city {city_id} - {err.reason}')
        return {'message': err.reason}, HTTPStatus.INTERNAL_SERVER_ERROR