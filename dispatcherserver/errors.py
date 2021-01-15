class ModelServerException(Exception):
    def __init__(self, message, http_code):
        self.message = message
        self.http_code = http_code


class InvalidInputException(ModelServerException):
    pass