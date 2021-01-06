from flask import Flask, jsonify
from http import HTTPStatus
from urllib.error import URLError


app = Flask(__name__)


@app.route('/')
def ping():
    return '', HTTPStatus.NO_CONTENT


@app.route('/cities/')
def get_available_cities():
    from proxy import get_key_storage_proxy

    storage_proxy = get_key_storage_proxy()
    cities = storage_proxy.get_available_model_servers()
    return jsonify(cities)


@app.route('/cities/<int:city_id>/weather')
def get_city_weather(city_id):
    from proxy import ModelProxy, get_key_storage_proxy

    try:
        storage_proxy = get_key_storage_proxy()
        model_address = storage_proxy.get_model_server_address(city_id)
        app.logger.debug(f'Stored address for {city_id}: {model_address}')
        model_proxy = ModelProxy(model_address)
        return jsonify(model_proxy.get_city_weather())
    except URLError as err:
        app.logger.error(f'Error for city {city_id} - {err.reason}')
        return {'message': err.reason}, HTTPStatus.INTERNAL_SERVER_ERROR