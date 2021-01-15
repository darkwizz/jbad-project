from dbaccess.jsonadapter import get_json_db_adapter

from flask import Flask, jsonify, request
from http import HTTPStatus
from datetime import date


app = Flask(__name__)

@app.route('/weather/history/current')
def get_current_weather_data():
    adapter = get_json_db_adapter()
    result = adapter.get_current_weather()
    return jsonify(result)


@app.route('/weather/history')
def get_historical_weather_data_for_dates():
    try:
        start_date = request.args.get(key='start_date', default=None, type=date.fromisoformat)
        end_date = request.args.get(key='end_date', default=None, type=date.fromisoformat)
    except ValueError:
        return {'message': 'Incorrect dates format'}, HTTPStatus.BAD_REQUEST
    
    if start_date is None and end_date is None:
        return {'message': 'Neither <start_date> nor <end_date> are passed'}, HTTPStatus.BAD_REQUEST
    
    start_date = start_date or end_date
    end_date = end_date or date.today()

    try:
        adapter = get_json_db_adapter()
    except ValueError as ex:
        app.logger.error(str(ex))
        return {'message': 'Env configuration problem'}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    try:
        result = adapter.get_weather_for_period(start_date, end_date)
        return jsonify(result)
    except ValueError as ex:
        return {'message': str(ex)}, HTTPStatus.BAD_REQUEST


@app.route('/weather/forecast')
def get_weather_forecast():
    return jsonify([])