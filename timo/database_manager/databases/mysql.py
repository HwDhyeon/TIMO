# -*- coding: utf-8 -*-

import datetime
import logging
import json
import os
import pymysql
import sys
import yaml
from typing import Any
from typing import Dict
from typing import Final
from typing import List
from typing import NoReturn
from typing import Union

from timo.database_manager.models import Database


QueryResult = Dict[str, Union[str, int, float]]
QueryResults = List[QueryResult]

LOG_PATH: Final[str] = os.path.dirname(__file__) + '/logs/mysql.log'

if os.path.isfile(LOG_PATH):
    os.remove(LOG_PATH)

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO, filemode='w',
    format='%(asctime)s:\n\t%(levelname)s:%(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

def _log_file_write(func):
    def wrapper(*args, **kwargs):
        path = func(*args, **kwargs)
        logging.info(f'Save success as query execution result file (path: {path})')
    return wrapper


class MySQL(Database):
    """MySQL Client"""

    def __init__(self, config) -> None:
        super(MySQL, self).__init__(config)
        self.db = config.db
        self.charset = config.charset

    def __connect__(self) -> NoReturn:
        try:
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db,
                charset=self.charset
            )
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        except pymysql.MySQLError as e:
            logging.error(e)
            print(f"Error connecting to MySQL Platform: {e}")
            sys.exit(1)
        else:
            logging.info('Database connection successful')

    def __commit__(self) -> NoReturn:
        try:
            self.conn.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
            sys.exit(2)
        else:
            logging.info('The changes have been reflected in the database.')

    def __disconnect__(self) -> NoReturn:
        self.__commit__()
        self.cursor.close()
        self.conn.close()
        logging.info('Database connection termination success')

    def _clean_datetime(self, query_result: Union[QueryResult, QueryResults]) -> str:
        """Converts a datetime object to a string when the column data type is DATETIME

        Args:
            query_result (Union[QueryResult, QueryResults]): [description]

        Returns:
            str: [description]
        """

        if isinstance(query_result, dict):
            query_result = [query_result]

        for i, result in enumerate(query_result):
            for key, value in result.items():
                if isinstance(value, datetime.datetime):
                    query_result[i][key] = value.strftime(r'%Y-%m-%d %H:%M:%S')
        return query_result

    def execute(self, query: str, *, args: Dict[str, Any]={}) -> NoReturn:
        try:
            self.__connect__()
            self.cursor.execute(query=query, args=args)
        except pymysql.MySQLError as e:
            print(e)
            logging.error(e)
            self.__disconnect__()
        else:
            logging.info(f'Query execution completed (Type: {query.upper().split()[0]})')

    def executemany(self, query: str, *, args: Dict[str, Any]={}) -> NoReturn:
        self.__connect__()
        self.cursor.executemany(query=query, args=args)
        self.__disconnect__()

    def execute_with_fetch_one(self, query: str, *, args: Dict[str, Any]={}) -> Dict[str, Union[str, int, float]]:
        self.execute(query=query, args=args)
        response: dict = self.cursor.fetchone()
        self.__disconnect__()
        clean_response = self._clean_datetime(response)
        return clean_response[0]

    def execute_with_fetch_many(self, query: str, size: int, *, args: Dict[str, Any]={}) -> Dict[str, Union[str, int, float]]:
        self.execute(query=query, args=args)
        response: dict = self.cursor.fetchmany(size=size)
        self.__disconnect__()
        clean_response = self._clean_datetime(response)
        return clean_response

    def execute_with_fetch_all(self, query: str, *, args: Dict[str, Any]={}) -> Dict[str, Union[str, int, float]]:
        self.execute(query=query, args=args)
        response: dict = self.cursor.fetchall()
        clean_response = self._clean_datetime(response)
        self.__disconnect__()
        return clean_response

    @_log_file_write
    def execute_save_json(self, query: str, path: str, *, args: Dict[str, Any]={}, encoding='utf-8') -> str:
        response = self.execute_with_fetch_all(query=query, args=args)
        with open(file=path, mode='w', encoding=encoding) as f:
            f.write(json.dumps(response, indent='\t', ensure_ascii=False))
        return path

    @_log_file_write
    def execute_save_yaml(self, query: str, path: str, *, args: Dict[str, Any]={}, encoding='utf-8') -> str:
        response = self.execute_with_fetch_all(query=query, args=args)
        with open(file=path, mode='w', encoding=encoding) as f:
            f.write(yaml.dump(response, indent=4, allow_unicode=True))
        return path

    def execute_save_yml(self, query: str, path: str, *, args: Dict[str, Any]={}, encoding='utf-8') -> str:
        self.execute_save_yaml(query=query, path=path, args=args, encoding=encoding)


if __name__ == "__main__":
    from config import Config
    mysql = MySQL(Config.mysql)
    # response = mysql.execute_with_fetch_all(query='select * from users')
    mysql.execute_save_json(query='select * from users', path='./results/sql.json')
    mysql.execute_save_yml(query='select * from users', path='./results/sql.yml')
