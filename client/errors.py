class ClientError(Exception):
    pass


class DataSynchronizationError(ClientError):
    pass


class ServerError(Exception):
    pass


class ServerUnavailableError(ServerError):
    pass


class NoSuchCityError(ServerError):
    pass


class NoWeatherForCityError(ServerError):
    pass


class ConfigurationError(Exception):
    pass