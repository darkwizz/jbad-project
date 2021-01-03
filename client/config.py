from datamanipulation import DataManipulator
from proxies import stub, server

import os


def get_data_processor():
    return DataManipulator()


def no_such_proxy(proxy_name):
    raise Exception(f'No such proxy: {proxy_name}')


def get_proxy():
    proxy_env = 'WEATHERPROXY'
    server_addr_env = 'WEATHERSERVER'
    proxies = {
        'stub': stub.ProxyStub,
        'server': server.ServerProxy
    }

    server_addr = os.getenv(server_addr_env, None)
    proxy_name = os.getenv(proxy_env, None)
    proxy_cls = proxies.get(proxy_name, lambda _: no_such_proxy(proxy_name))
    proxy = proxy_cls(server_addr)
    return proxy
