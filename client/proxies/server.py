

class ServerProxy:
    def __init__(self, server_address):
        raise NotImplemented
        self._server_ip = server_address
    
    def load_available_cities(self):
        raise NotImplemented
    
    def load_city_weather(self, city_id):
        raise NotImplemented
