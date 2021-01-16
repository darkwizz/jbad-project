from errors import ClientError, DataSynchronizationError, ServerError

import time
import os
from datetime import date


def print_menu(menu_items):
    menu = '\n'.join(menu_items)
    print(menu)


def incorrect_choice(*args):
    print('No such option')


def wait():
    print('Waiting...')
    time.sleep(5)


def clear_scr():
    if os.name == 'posix':
        os.system('clear')


def read_date(prompt_msg):
    prompt = f'{prompt_msg} (YYYY-MM-DD) or "{CANCEL_CHOICE}" to go back: '
    date_str = input(prompt)
    if date_str == CANCEL_CHOICE:
        return date_str
    try:
        _ = date.fromisoformat(date_str)
        return date_str
    except ValueError:
        raise ClientError('Incorrect date format')


def read_items_index(items_len, item_name):
    choice = input(f'Enter {item_name} index (or "{CANCEL_CHOICE}" to go back to the main menu): ')
    if choice == CANCEL_CHOICE:
        return choice
    if not choice.isnumeric():
        raise ClientError('Must be a number')
    choice = int(choice)
    if choice < 1 or choice > items_len:
        raise ClientError(f'{item_name.capitalize()} index must be in the proper range')
    return choice


CANCEL_CHOICE = 'cancel'
def read_visualization_save_path():
    save_path = input(f'Enter visualization save path (or "{CANCEL_CHOICE}" to go back to the main menu): ')
    return save_path


class Client:
    main_menu_items = [
        '1 - load city list',
        '2 - show loaded cities',
        '3 - show city current weather',
        '4 - load historical weather statistics for a city',
        '5 - visualize last loaded data',
        '0 - exit'
    ]

    def __init__(self, server_proxy, data_manipulator):
        if server_proxy is None or data_manipulator is None:
            raise ValueError('Server proxy and data manipulation component should be defined')

        self._server_proxy = server_proxy
        self._data_manipulator = data_manipulator
        self._session = {}
        self._functions = {
            '1': self._load_city_list,
            '2': self._print_loaded_cities,
            '3': self._print_city_current_weather,
            '4': self._load_city_weather,
            '5': self._visualize_last_lodaded_weather
        }
    
    def _load_city_list(self):
        cities = self._server_proxy.load_available_cities()
        self._session['cities'] = cities
        print(f'Loaded {len(cities)} available cities')
    
    def _print_loaded_cities(self):
        cities = self._session.get('cities', None)
        if cities is None:
            raise ClientError('No cities loaded. Load them first')
        for i, city in enumerate(cities):
            print(f'{i + 1}. {city["name"]}')
    
    def __get_selected_city_index(self):
        cities = self._session.get('cities', [])
        if len(cities) == 0:
            raise ClientError('No available or loaded cities')
        
        city_index = read_items_index(len(cities), 'city')
        return city_index
    
    def _print_city_current_weather(self):
        city_index = self.__get_selected_city_index()
        if city_index == CANCEL_CHOICE:
            return
        city = self._session['cities'][city_index - 1]
        weather = self._server_proxy.load_city_current_weather(city['id'])
        print(weather)
    
    def _load_city_weather(self):
        city_index = self.__get_selected_city_index()
        if city_index == CANCEL_CHOICE:
            return
        city = self._session['cities'][city_index - 1]

        start_date = read_date('Read start date')
        if start_date == CANCEL_CHOICE:
            return
        
        end_date = read_date('Read end date')
        if end_date == CANCEL_CHOICE:
            return
        
        weather = self._server_proxy.load_city_weather(city['id'], start_date, end_date)
        data_hash = self._data_manipulator.update_data(weather)
        self._session['loaded_data_hash'] = data_hash
        print(f'Loaded {len(self._data_manipulator)} rows')
    
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
        if param_index == CANCEL_CHOICE:
            return
        param = params_list[param_index - 1]
        save_path = read_visualization_save_path()
        if save_path == CANCEL_CHOICE:
            return
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
            except (ClientError, ServerError) as ex:
                print(ex)
            wait()
        print('Quitting...')
        print('GOODBYE')
