from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/weather/history')
def get_historical_weather_data():
    return jsonify([])


@app.route('/weather/forecast')
def get_weather_forecast():
    return jsonify([])