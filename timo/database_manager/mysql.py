from colors import color
from timo.decorator import timer
from typing import Any
from typing import AnyStr
from typing import Dict
from typing import List
from typing import NoReturn
from typing import Tuple
from typing import Union
import csv
import json
import os
import pymysql
import time
import yaml

def colored_print(msg: AnyStr, color_name: AnyStr, end='\n') -> NoReturn:
    """
    Apply color to the print function.

        Parameters:
            msg (str):        Message to print
            color_name (str): Color
            end (str) :       Same as end parameter of print function

        Returns
        
    """
    print(color(msg, color_name), end=end)


class MySQL(object):
    @timer
    def open_DB_session(self) -> NoReturn:
        def _read_DB_info() -> Dict:
            with open(file=os.getcwd() + '/data/db.json', mode='r', encoding='utf-8') as db:
                return json.load(db)
        try:
            colored_print('Connecting DB...', 'yellow')
            self.db_info: dict = _read_DB_info()
            self.conn: pymysql.Connection = pymysql.connect(
                host = self.db_info['host'],
                port = self.db_info['port'],
                user = self.db_info['user'],
                passwd = self.db_info['passwd'],
                db = self.db_info['db']
            )
            self.cursor: pymysql.cursors.Cursor = self.conn.cursor()
        except Exception as e:
            colored_print(e, 'red')
            self.cursor.close()
            self.conn.close()
        else:
            colored_print('Done', 'green')

    def close_DB_session(self) -> NoReturn:
        try:
            self.conn.commit()
            self.conn.close()
            self.cursor.close()
        except Exception as e:
            colored_print(e, 'red')

    @timer
    def send_query(self, sql: AnyStr, type: Union['select', 'insert', 'delete', 'update'], save=None) -> NoReturn:
        def get_column_names(cursor: pymysql.cursors.Cursor) -> List[AnyStr]:
            return [i[0] for i in cursor.description]

        def _on_save(save: AnyStr, result: List[Tuple[Any]]) -> bool:
            def _save(path: str, data: Any) -> NoReturn:
                ext: str = path.split('.')[-1]
                colored_print('Save query result...', 'yellow')
                colored_print(f'File ext: {ext}', 'yellow', end='\n\n')
                with open(file=path, mode='w', encoding='utf-8', newline='') as f:
                    if ext == 'csv' or ext == 'txt':
                        wr = csv.writer(f)
                        wr.writerows(data)
                    else:
                        f.write(data)

            def _compression(columns, rows):
                r = []
                for row in rows:
                    r.append(dict(zip(columns, row)))
                return r

            if save is not None:
                colored_print('Parse query result...', 'yellow', end='\n\n')
                data = None
                columns: list = get_column_names(cursor=self.cursor)
                if save == 'json':
                    data = json.dumps(_compression(columns, result), indent='\t')
                elif save == 'yaml' or save == 'yml':
                    data = yaml.dump(_compression(columns, result), indent=4)
                elif save == 'csv':
                    data = [columns]
                    for row in list(result):
                        data.append(row)
                else:
                    if save != 'txt':
                        colored_print('현재 지원되지 않는 파일 형식입니다.', 'red', end='\t')
                        colored_print(f'(입력된 파일 형식: {save})', 'red')
                        colored_print('sql.txt 파일로 대체됩니다.', 'red', end='\n\n')
                        save = 'txt'
                    data = [columns]
                    for row in list(result):
                        data.append(row)
                _save(f'./out.{save}', data)
                return True
            else:
                return False
        self.cursor.execute(sql)
        colored_print('Sending query...', 'yellow', end='\n\n')
        try:
            if type == 'select':
                result: list = list(self.cursor.fetchall())
                columns: list = get_column_names(cursor=self.cursor)
                if not _on_save(save, result):
                    print(' │ ' + ' │ '.join(columns) + ' │ ')
                    for row in result:
                        print(' │ ' + ' │ '.join(map(str, row)) + ' │ ')
            else:
                pass
        except Exception as e:
            colored_print(e, 'red')
        else:
            colored_print('Done', 'green')


if __name__ == "__main__":
    sql = """SELECT
        *
        FROM
            JENKINS_BUILD_RESULT
    WHERE
        PROJECT_NM = 'IRIS-E2E-SAAS'
        AND
        BUILD_NO = (SELECT MAX(BUILD_NO) FROM JENKINS_BUILD_RESULT WHERE PROJECT_NM = 'IRIS-E2E-SAAS')"""
    db: MySQL = MySQL()
    db.open_DB_session()
    db.send_query(sql=sql, type='select', save='tess')
    db.close_DB_session()
