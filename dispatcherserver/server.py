from flask import Flask, jsonify
from http import HTTPStatus


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

    storage_proxy = get_key_storage_proxy()
    model_address = storage_proxy.get_model_server_address(city_id)
    model_proxy = ModelProxy(model_address)
    return jsonify(model_proxy.get_city_weather())