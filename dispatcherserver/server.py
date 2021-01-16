from errors import ModelServerException

from flask import Flask, jsonify, request
from http import HTTPStatus
from urllib.error import URLError
from datetime import date


app = Flask(__name__)


def validate_city_request_proxy_errors(api_view):
    def wrapper(city_id, *args, **kwargs):
        try:
            response = api_view(city_id, *args, **kwargs)
            return response
        except URLError as err:
            app.logger.error(f'Error for city {city_id} - {err.reason}')
            return {'message': err.reason}, HTTPStatus.INTERNAL_SERVER_ERROR
        except ModelServerException as ex:
            app.logger.error(f'Error for city {city_id} - {ex.message}')
            return {'message': ex.message}, ex.http_code
        except Exception as ex:
            app.logger.error(f'Internal error for city {city_id} - {str(ex)}')
            return {'message': 'Internal server error'}, HTTPStatus.INTERNAL_SERVER_ERROR
    wrapper.__qualname__ = api_view.__qualname__
    wrapper.__name__ = api_view.__name__
    return wrapper


def get_model_server_proxy(server_id):
    from proxy import ModelProxy, get_key_storage_proxy

    storage_proxy = get_key_storage_proxy()

    if not storage_proxy.model_server_available(server_id):
        raise ModelServerException('No such city', HTTPStatus.BAD_REQUEST)

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
@validate_city_request_proxy_errors
def get_city_current_weather(city_id):
    model_proxy = get_model_server_proxy(city_id)
    result = model_proxy.get_city_current_weather()
    return jsonify(result)


@app.route('/cities/<int:city_id>/weather')
@validate_city_request_proxy_errors
def get_city_weather(city_id):
    try:
        start_date = request.args.get(key='start_date')
        end_date = request.args.get(key='end_date')
        
        start_date = date.fromisoformat(start_date) if start_date else date.today()
        end_date = date.fromisoformat(end_date) if end_date else date.today()

        if start_date > date.today() or end_date > date.today():
            return {'message': 'Historical weather cannot be requested for dates in the future'}, HTTPStatus.BAD_REQUEST

        if start_date > end_date:
            return {'message': 'Start date should not be later than end date'}, HTTPStatus.BAD_REQUEST

        model_proxy = get_model_server_proxy(city_id)
        result = model_proxy.get_city_weather(start_date, end_date)
        return jsonify(result)
    except ValueError:
        return {'message': 'Incorrect dates format'}, HTTPStatus.BAD_REQUEST
