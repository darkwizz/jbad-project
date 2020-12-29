import citylist
from datasource import jsonweather

import os
import matplotlib.pyplot as plt


class Session:
    def __init__(self, datasource):
        self._cities_list = get_available_regions()
        self._data = datasource
        self.current_column = None
    
    def get_top_regions(self, top_n=10):
        return self._cities_list[:top_n]
    
    def get_region(self, index):
        if index < 0 or index > len(self._cities_list):
            raise IndexError('No city with this index')
        return self._cities_list[index]
    
    @property
    def data(self):
        return self._data


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


FUNCTIONS = {
    '0': app_exit,
    '1': print_regions_list,
    '2': show_region_weather
}


def incorrect_choice(*args):
    print('No such option')


def main(*args):
    import time

    json_path = jsonweather.get_weather_json_path()
    data = jsonweather.read_weather_json(json_path)
    session = Session(data)
    while True:
        try:
            clear_scr()
            print_menu()
            choice = input("Choose one option: ")
            func = FUNCTIONS.get(choice, incorrect_choice)
            func(session)
        except (ValueError, TypeError) as err:
            print(err)
        time.sleep(5)


if __name__ == '__main__':
    import sys

    main(*sys.argv)