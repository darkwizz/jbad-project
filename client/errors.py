class ClientError(Exception):
    pass


class DataSynchronizationError(ClientError):
    pass


class ServerError(Exception):
    pass


class NoSuchCityError(ServerError):
    pass