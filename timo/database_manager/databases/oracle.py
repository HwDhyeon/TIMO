from decorators import timer
from file_manager.file_reader import Reader
from typing import NoReturn
from utils import colored_print
import cx_Oracle
import os


class Oracle(object):
    def __init__(self):
        self.reader = Reader()

    @timer
    def open_DB_session(self) -> NoReturn:
        def _read_DB_info() -> dict:
            return self.reader.read_json_file( os.getcwd() + '/data/db.json')

        try:
            colored_print('Connecting DB...', 'yellow')
            self.db_info = _read_DB_info()['oracle']
            
            db_host = self.db_info['host'] + '@' + self.db_info['port'] + '/' + self.db_info['sid']
            self.conn = cx_Oracle.connect(
                self.db_info['user'],
                self.db_info['password'],
                db_host
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            colored_print(e, 'red')
        else:
            colored_print('Done', 'green')

    def close_DB_session(self) -> NoReturn:
        try:
            self.conn.commit()
            self.conn.close()
            self.cursor.close()
        except Exception as e:
            print(e, 'red')
