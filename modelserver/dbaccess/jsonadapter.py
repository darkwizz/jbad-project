import os


def get_json_db_adapter():
    db_path = os.getenv('WATHER_DB_PATH')
    return JsonWeatherDbAdapter(db_path)


class JsonWeatherDbAdapter:
    def __init__(self, dbpath):
        if not dbpath or not os.path.exists(dbpath):
            raise ValueError('No DB by this path')
        self._dbpath = dbpath