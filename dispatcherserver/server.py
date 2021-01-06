from flask import Flask, jsonify
from http import HTTPStatus

app = Flask(__name__)


@app.route('/')
def ping():
    return '', HTTPStatus.NO_CONTENT


@app.route('/cities/')
def get_available_cities():
    return jsonify([])


@app.route('/cities/<int:city_id>/weather')
def get_city_weather(city_id):
    return jsonify([])