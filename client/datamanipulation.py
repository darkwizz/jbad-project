import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import os

from errors import ClientError


class DataManipulator:
    def __init__(self, data=None):
        """
        Input parameters:
        - data - dict or list
        """
        if data is not None:
            self._data = DataManipulator._process_input_data(data, self.date_column)
        else:
            self._data = None
    
    @property
    def date_column(self):
        return 'datetime'
    
    @property
    def data_hash(self):
        if self._data is None:
            raise ClientError('Initialize data first')
        return id(self._data)
    
    def update_data(self, data):
        self._data = DataManipulator._process_input_data(data, self.date_column)
        return self.data_hash
    
    def get_parameters_list(self):
        if self._data is None:
            raise ClientError('Initialize data first')
        data_columns = self._data.columns
        result = list(filter(lambda x: x != self.date_column, data_columns))
        return result

    def visualize_weather_parameter(self, parameter, save_path=''):
        if self._data is None:
            raise ClientError('Initialize data first')

        if parameter not in self.get_parameters_list():
            raise ClientError('This parameter does not exist')

        if not DataManipulator._visualization_path_valid(save_path):
            raise ClientError('Passed graph image path is not valid')

        x_col = self.date_column
        X = self._data[x_col].apply(lambda x: x.hour)
        Y = self._data[parameter]
        plt.plot(X, Y)
        plt.xlabel('Hours')
        plt.ylabel(parameter)
        # plt.legend()
        # plt.show()  # requires some GUI matplotlib backend
        plt.savefig(save_path)  # when matplotlib backend is non-GUI (like 'agg')
    
    def __len__(self):
        length = len(self._data) if self._data is not None else 0
        return length

    @staticmethod
    def _visualization_path_valid(path):
        ext_len = len('.png')
        if not path or len(path) < ext_len:
            return False
        
        dirname = os.path.dirname(path) or '.'
        dir_exists = os.path.exists(dirname)
        extenstion_correct = path[-ext_len:] == '.png'
        return dir_exists and extenstion_correct

    @staticmethod
    def _process_input_data(data, date_column):
        datetime_columns = ['sunrise', 'sunset']
        df = pd.DataFrame(data)
        df[date_column] = pd.to_datetime(df[date_column])
        for dt_col in datetime_columns:
            df[dt_col] = df[dt_col].apply(lambda x: dt.datetime.fromtimestamp(x))
        return df


if __name__ == '__main__':
    from proxies.stub import get_test_city_weather
    
    weather = get_test_city_weather()
    data_process = DataManipulator(weather)
    columns = data_process.get_parameters_list()
    print(f'Available columns: {columns}')
    column = input('Enter column: ')
    save_path = input('Enter visualization save path: ')
    data_process.visualize_weather_parameter(column, save_path)
    print('SUCCESS')