import citylist
from datasource import jsonweather
from errors import ClientError, DataSynchronizationError

import time
import os
import matplotlib.pyplot as plt


def print_menu(menu_items):
    menu = '\n'.join(menu_items)
    print(menu)


def incorrect_choice(*args):
    print('No such option')


def wait():
    time.sleep(5)


def read_items_index(items_len, item_name):
    choice = input(f'Enter {item_name} index: ')
    if not choice.isnumeric():
        raise ClientError('Must be a number')
    choice = int(choice)
    if choice < 1 or choice > items_len:
        raise ClientError(f'{item_name.capitalize()} index must be in the proper range')
    return choice


class Client:
    main_menu_items = [
        '1 - load city list',
        '2 - show loaded cities',
        '3 - load weather statistics for a city',
        '4 - visualize last loaded data',
        '0 - exit'
    ]

    def __init__(self, server_proxy, data_manipulator):
        if not server_proxy or not data_manipulator:
            raise ValueError('Server proxy and data manipulation component should be defined')

        self._server_proxy = server_proxy
        self._data_manipulator = data_manipulator
        self._session = {}
        self._functions = {
            '1': self._load_city_list,
            '2': self._print_loaded_cities,
            '3': self._load_city_weather,
            '4': self._visualize_last_lodaded_weather
        }
    
    def _load_city_list(self):
        cities = self._server_proxy.load_cities()
        self._session['cities'] = cities
        print(f'Loaded {len(cities)} available cities')
    
    def _print_loaded_cities(self):
        cities = self._session.get('cities', None)
        if cities is None:
            raise ClientError('No cities loaded. Load them first')
        for i, city in enumerate(cities):
            print(f'{i + 1}. {city}')
    
    def _load_city_weather(self):
        cities = self._session.get('cities', [])
        if len(cities) == 0:
            raise ClientError('No available or loaded cities')
        
        city_index = read_items_index(len(cities), 'city')
        city = cities[city_index - 1]
        weather = self._server_proxy.load_city_weather(city)
        data_hash = self._data_manipulator.update_data(weather)
        self._session['loaded_data_hash'] = data_hash
    
    def _visualize_last_lodaded_weather(self):
        last_data_hash = self._session.get('loaded_data_hash', None)
        if not last_data_hash:
            raise ClientError('No weather loaded')
        if last_data_hash != self._data_manipulator.data_hash:
            raise DataSynchronizationError('Loaded data is not synchronized with visualizer')
        
        print('Available parameters:')
        params_list = self._data_manipulator.get_parameters_list()
        for i, param in enumerate(params_list):
            print(f'{i + 1}. {param}')
        param_index = read_items_index(len(params_list), 'parameter')
        param = params_list[param_index - 1]
        save_path = read_visualization_save_path()
        self._data_manipulator.visualize_weather_parameter(param, save_path=save_path)
    
    def run(self):
        while True:
            try:
                clear_scr()
                print_menu(self.main_menu_items)
                choice = input('Choose option: ')
                if choice == '0':
                    break
                func = self._functions.get(choice, incorrect_choice)
                func()
            except ClientError as ex:
                print(ex)
            wait()
        print('Quitting...')
        print('GOODBYE')


def print_menu():
    menu = \
    """1 - get regions list;
2 - show weather stats for a region;
0 - exit;
    """
    print(menu)


def app_exit(session):
    print('Quitting...')
    print('GOODBYE')
    exit(0)


def clear_scr():
    clear_cmd = 'clear' if os.name == 'posix' else 'cls'
    os.system(clear_cmd)


def print_regions_list(session):
    regions = session.get_top_regions(top_n=10)
    regions_str = '\n'.join([
        f'{i + 1}. {region}' for i, region in enumerate(regions)
    ])
    print(regions_str)


def get_available_regions(top_n=-1):
    citylist_path = citylist.get_city_list_json_path()
    cities = citylist.get_city_list(citylist_path)
    return cities[:top_n]


def show_region_weather(session):
    choice_str = input('Enter region number: ')
    if not choice_str.isnumeric():
        print('Invalid input')
        return
    region_index = int(choice_str)
    region = session.get_region(region_index)
    region_weather = get_region_weather(session, region.get_city_id())
    visualize_region_weather(region_weather, session.current_column)


def get_region_weather(session, region_id):
    weather_columns = session.data.get_hourly_weather_columns()
    session.current_column = weather_columns[0]
    weather = session.data.get_today_hourly_column(weather_columns[0])
    return weather


def visualize_region_weather(region_weather, column_name):
    sorted_weather = sorted(region_weather)
    X = sorted_weather
    Y = [region_weather[hour] for hour in X]
    plt.plot(X, Y)
    plt.xlabel('Hours')
    plt.ylabel(column_name)
    # plt.legend()
    # plt.show()  # requires some GUI matplotlib backend
    plot_path = 'weather_plot.png'
    plt.savefig(plot_path)  # when matplotlib backend is non-GUI (like 'agg')
