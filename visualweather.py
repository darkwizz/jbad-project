from client.weathercli import Client as ConsoleClient

import argparse


CLIENT_CHOICES = {
    'cli': ConsoleClient,
    'gui': lambda *args: print('NOT IMPLEMENTED')
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', default='cli', choices=CLIENT_CHOICES.keys(),\
        help='Type of client, can be console or graphical')
    args = parser.parse_args()

    print('WELCOME IN VISUALWEATHER APP')
    print(f'Selected client type is {args.client}')
    client_cls = CLIENT_CHOICES[args.client]
    # client = client_cls(server_proxy, data_manipulator)


if __name__ == '__main__':
    main()