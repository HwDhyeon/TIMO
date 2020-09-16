from typing import Any
from typing import Dict


class Database(object):
    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.user = config['user']
        self.password = config['password']

    def __connect__(self):
        pass

    def __commit__(self):
        pass

    def __disconnect__(self):
        pass

    def execute(self, query: str, *, args: Dict[str, Any]={}):
        pass

    def executemany(self, query: str, *, args: Dict[str, Any]={}):
        pass

    def execute_with_fetch_one(self, query: str, *, args: Dict[str, Any]={}):
        pass

    def execute_with_fetch_many(self, query: str, size: int, *, args: Dict[str, Any]={}):
        pass

    def execute_with_fetch_all(self, query: str, *, args: Dict[str, Any]={}):
        pass

    def execute_save_json(self, query: str, path: str, *, args: Dict[str, Any]={}, encoding='utf-8'):
        pass

    def execute_save_yaml(self, query: str, path: str, *, args: Dict[str, Any]={}, encoding='utf-8'):
        pass

    def execute_save_yml(self, query: str, path: str, *, args: Dict[str, Any]={}, encoding='utf-8'):
        self.execute_save_yaml(query=query, path=path, args=args, encoding=encoding)
