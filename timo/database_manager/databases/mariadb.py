# -*- coding: utf-8 -*-

import datetime
import logging
import mariadb
import json
import os
import sys
import yaml
from typing import Any
from typing import Dict
from typing import Final
from typing import List
from typing import NoReturn
from typing import Tuple
from typing import Union

from timo.database_manager.models import Database


Arguments = Tuple[Union[str, int, float]]
QueryResult = Tuple[Union[str, int, float]]
QueryResults = List[QueryResult]
ZippedQueryResult = List[Dict[str, Union[str, int, float]]]

LOG_PATH: Final[str] = os.path.dirname(__file__) + '/logs/mariadb.log'

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


class MariaDB(Database):

    def __init__(self, config) -> None:
        super(MariaDB, self).__init__(config)
        self.db = config.db

    # Connect to MariaDB Platform
    def __connect__(self) -> NoReturn:
        """ABC"""

        try:
            self.conn = mariadb.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db
            )
            self.conn.autocommit = False
            # Get Cursor
            self.cursor = self.conn.cursor(named_tuple=False)
        except mariadb.Error as e:
            logging.error(e)
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        else:
            logging.info('Database connection successful')

    # Create Commit
    def __commit__(self) -> NoReturn:
        try:
            self.conn.commit()
        except mariadb.Error as e:
            logging.error(e)
            sys.exit(1)
        else:
            logging.info('The changes have been reflected in the database.')

    # Close Connection 
    def __disconnect__(self) -> NoReturn:
        self.cursor.close()
        self.__commit__()
        self.conn.close()
        logging.info('Database connection termination success')

    def _make_response(self, query_result: QueryResults) -> ZippedQueryResult:
        if isinstance(query_result, tuple):
            query_result = [query_result]
        columns = [column[0] for column in self.cursor.description]
        response: ZippedQueryResult = [{key:value for key, value in zip(columns, result)} for result in query_result]
        return response


    def execute(self, query: str, *, args: Tuple[int, str, float]=()) -> NoReturn:        
        try:
            self.__connect__()
            self.cursor.execute(query, args)
        except mariadb.Error as e:
            print(e)
            logging.error(e)
            self.__disconnect__()
        else:
            logging.info(f'Query execution completed (Type: {query.upper().split()[0]})')

    def execute_with_fetch_one(self, query: str, *, args: Arguments=()) -> list:
        self.execute(query=query, args=args)
        query_result: QueryResult = self.cursor.fetchone()
        response = self._make_response(query_result)
        self.__disconnect__()
        return response

    def execute_with_fetch_many(self, query: str, size: int, *, args: Arguments=()) -> list:
        self.execute(query=query, args=args)
        query_result: QueryResults = self.cursor.fetchmany(size=size)        
        response = self._make_response(query_result)
        self.__disconnect__()
        return response

    def execute_with_fetch_all(self, query: str, *, args: Arguments=()) -> list:
        self.execute(query=query, args=args)
        query_result: QueryResults = self.cursor.fetchall()
        response = self._make_response(query_result)
        self.__disconnect__()
        return response

    @_log_file_write
    def execute_save_json(self, query: str, path: str, *, args: Arguments=(), encoding: str='utf-8') -> NoReturn:
        response = self.execute_with_fetch_all(query=query, args=args)
        with open(file=path, mode='w', encoding=encoding) as f:
            f.write(json.dumps(response, indent='\t', ensure_ascii=False))
        return path

    @_log_file_write
    def execute_save_yaml(self, query: str, path: str, *, args: Arguments=(), encoding='utf-8') -> NoReturn:
        response = self.execute_with_fetch_all(query=query, args=args)
        with open(file=path, mode='w', encoding=encoding) as f:
            f.write(yaml.dump(response, indent=4, allow_unicode=True))
        return path

    def execute_save_yml(self, query: str, path: str, *, args: Arguments=(), encoding='utf-8') -> NoReturn:
        self.execute_save_yaml(query=query, path=path, args=args, encoding=encoding)



if __name__ == "__main__":
    from config import Config
    query = "SELECT * FROM JENKINS_BUILD_RESULT WHERE PROJECT_NM = 'IRIS-E2E' AND BUILD_NO = (SELECT MAX(BUILD_NO) FROM JENKINS_BUILD_RESULT WHERE PROJECT_NM = 'IRIS-E2E')"
    db = MariaDB(config=Config.mariadb)
    response = db.execute_with_fetch_one(query)
    print(response)
