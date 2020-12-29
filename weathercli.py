import citylist

import os


def print_menu():
    menu = \
    """1 - get regions list;
2 - show weather stats for a region;
0 - exit;
    """
    print(menu)


def app_exit():
    print('Quitting...')
    print('GOODBYE')
    exit(0)


def clear_scr():
    clear_cmd = 'clear' if os.name == 'posix' else 'cls'
    os.system(clear_cmd)


def print_regions_list():
    regions = get_available_regions()
    regions_str = '\n'.join([
        f'{i + 1}. {region}' for i, region in enumerate(regions)
    ])
    print(regions_str)


def get_available_regions():
    citylist_path = citylist.get_city_list_json_path()
    cities = citylist.get_city_list(citylist_path)
    return cities


def show_region_weather():
    choice_str = input('Enter region number: ')
    if not choice_str.isnumeric():
        print('Invalid input')
        return
    region_id = int(choice_str)
    region_weather = get_region_weather(region_id)
    visualize_region_weather(region_weather)


def get_region_weather(region_id):
    return []


def visualize_region_weather(region_weather):
    print(region_weather)


FUNCTIONS = {
    '0': app_exit,
    '1': print_regions_list,
    '2': show_region_weather
}


def incorrect_choice():
    print('No such option')


def main(*args):
    import time

    while True:
        clear_scr()
        print_menu()
        choice = input("Choose one option: ")
        func = FUNCTIONS.get(choice, incorrect_choice)
        func()
        time.sleep(5)


if __name__ == '__main__':
    import sys

    main(*sys.argv)