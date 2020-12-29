import citylist
from datasource import jsonweather

import os


class Session:
    def __init__(self):
        self._cities_list = get_available_regions()
    
    def get_top_regions(self, top_n=10):
        return self._cities_list[:top_n]
    
    def get_region(self, index):
        if index < 0 or index > len(self._cities_list):
            raise IndexError('No city with this index')
        return self._cities_list[index]


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
    region_weather = get_region_weather(region.get_city_id())
    visualize_region_weather(region_weather)


def get_region_weather(region_id):
    json_path = jsonweather.get_weather_json_path()
    data = jsonweather.read_weather_json(json_path)
    return data.get_today_hourly()


def visualize_region_weather(region_weather):
    print(region_weather)


FUNCTIONS = {
    '0': app_exit,
    '1': print_regions_list,
    '2': show_region_weather
}


def incorrect_choice(*args):
    print('No such option')


def main(*args):
    import time

    session = Session()
    while True:
        try:
            clear_scr()
            print_menu()
            choice = input("Choose one option: ")
            func = FUNCTIONS.get(choice, incorrect_choice)
            func(session)
        except Exception as ex:
            print(ex)
        time.sleep(5)


if __name__ == '__main__':
    import sys

    main(*sys.argv)