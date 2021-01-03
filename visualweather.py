from client.weathercli import Client as ConsoleClient
from client.datamanipulation import DataManipulator
from client.proxies.stub import ProxyStub
from client import config

import argparse


def gui_client(*args):
    raise NotImplemented('GUI client is not implemented')

CLIENT_CHOICES = {
    'cli': ConsoleClient,
    'gui': gui_client
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', default='cli', choices=CLIENT_CHOICES.keys(),\
        help='Type of client, can be console or graphical')
    args = parser.parse_args()

    print('WELCOME IN VISUALWEATHER APP')
    print(f'Selected client type is {args.client}')
    client_cls = CLIENT_CHOICES[args.client]
    data_manipulator = config.get_data_processor()
    proxy = config.get_proxy()
    client = client_cls(proxy, data_manipulator)
    client.run()


if __name__ == '__main__':
    main()