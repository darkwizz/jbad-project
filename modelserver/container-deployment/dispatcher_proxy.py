import requests
import argparse
import os


def register_model_in_dispatcher(city_id, dispatcher_url, city_name, model_url):
    request_body = {
        'name': city_name,
        'host': model_url
    }
    url = os.path.join(dispatcher_url, 'models', city_id, 'checkpoint')
    response = requests.post(url, json=request_body)
    if response.status_code == 200:
        result = response.json()
        refresh_time = result.get('refresh_time')
        print(refresh_time)
    

def refresh_model_in_dispatcher(city_id, dispatcher_url):
    url = os.path.join(dispatcher_url, 'models', city_id, 'checkpount')
    response = requests.put(url)
    if response.status_code != 204:
        raise Exception(f'Some error happened.\n{str(response.text)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--register', action='store_true')
    group.add_argument('--refresh', action='store_true')
    parser.add_argument('-c', '--cityid', required=True)
    parser.add_argument('-d', '--dispatcher', required=True)
    parser.add_argument('-n', '--cityname')
    parser.add_argument('-m', '--model')
    args = parser.parse_args()

    city_id = args.cityid
    dispatcher = args.dispatcher

    if args.register:
        city_name = args.cityname
        model_url = args.model
        if city_name is None or model_url is None:
            raise argparse.ArgumentError('For --register must be specified cityname and model')
        register_model_in_dispatcher(city_id, dispatcher, city_name, model_url)
    elif args.refresh:
        refresh_model_in_dispatcher(city_id, dispatcher)
