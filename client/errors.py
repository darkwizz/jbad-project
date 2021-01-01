class ClientError(Exception):
    pass


class DataSynchronizationError(ClientError):
    pass