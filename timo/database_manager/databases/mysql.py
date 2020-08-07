"""Connect to MySQL and execute various queries."""

from timo.decorators import timer
from typing import Any
from typing import AnyStr
from typing import Dict
from typing import List
from typing import NoReturn
from typing import Tuple
from timo.utils import colored_print
import csv
import json
import os
import pymysql
import yaml


class MySQL(object):
    """MySQL"""

    @timer
    def open_DB_session(self) -> NoReturn:
        """Try to access the database."""

        def _read_DB_info() -> Dict:
            """Read information needed to access the database."""

            with open(file=os.getcwd() + '/data/db.json', mode='r', encoding='utf-8') as db:
                return json.load(db)
        try:
            colored_print('Connecting DB...', 'yellow')
            self.db_info: dict = _read_DB_info()['mysql']
            self.conn: pymysql.Connection = pymysql.connect(
                host=self.db_info['host'],
                port=self.db_info['port'],
                user=self.db_info['user'],
                password=self.db_info['password'],
                db=self.db_info['db']
            )
            self.cursor: pymysql.cursors.Cursor = self.conn.cursor()
        except Exception as e:
            colored_print(e, 'red')
        else:
            colored_print('Done', 'green')

    def close_DB_session(self) -> NoReturn:
        """Terminate the connection to the database."""

        try:
            self.conn.commit()
            self.conn.close()
            self.cursor.close()
        except Exception as e:
            colored_print(e, 'red')

    @timer
    def send_query(self, sql: AnyStr, type: str, args=[], save=None) -> NoReturn:
        """
        Pass SQL query statements to the database.

            Paramaters:
                sql(str): SQL query statement.
                          Dynamic delivery is not possible and must first be converted to plaintext.
                type(str['select', 'insert', 'delete', 'update']): The format of the SQL query statement.
                save(str, None): Determines whether to save results when the SQL query is select.
                                 If None, it is displayed on the screen.
                                 If you enter a file format, the file is saved in that format.
                                 The default value is None.
                                 If it does not match the supported format, it is saved as txt.
                                 Supported formats: ['csv', 'json', 'yaml', 'yml', 'txt']
        """

        def _get_column_names(cursor: pymysql.cursors.Cursor) -> List[AnyStr]:
            """
            Get the column names of a table.

                Parameters:
                    cursor(pymysql.cursors.Cursor): Cursor object associated with MySQL.

                Returns:
                    list: Returns a list of strings containing column names.
            """
            return [i[0] for i in cursor.description]

        def _on_save(save: AnyStr, result: List[Tuple[Any]]) -> bool:
            """
            Decide whether to save the results of the query to a file.

                Parameters:
                    save(srt): The default value is None, in which case the results are not saved to a file.
                               The supported formats are: ['json', 'yaml', 'yml', 'csv', 'txt']
                               If any other format is entered, it is converted to txt.

                    result(List[Tuple]): A list that contains the results of the query.

                Returns:
                    bool: Returns True if saved as a file, False otherwise.

            """

            def _save(path: str, data: Any) -> NoReturn:
                """
                Save the input data in the designated format.

                    Parameters:
                        path(str): Where the file will be saved
                        data(any): Raw data to be saved to file
                """

                ext: str = path.split('.')[-1]
                colored_print('Save query result...', 'yellow')
                colored_print(f'File ext: {ext}', 'yellow', end='\n\n')
                with open(file=path, mode='w', encoding='utf-8', newline='') as f:
                    if ext == 'csv' or ext == 'txt':
                        wr = csv.writer(f)
                        wr.writerows(data)
                    else:
                        f.write(data)

            def _compression(columns: list, rows: list) -> List[Dict]:
                """
                Compress the query result into a list in the form of { column: value }

                    Parameters:
                        columns(list): Table column names
                        rows(list): Query results
                    Returns:
                        list(dict): A list converted to a dictionary of type { column: value }
                """

                r = []
                for row in rows:
                    r.append(dict(zip(columns, row)))
                return r

            if save is not None:
                colored_print('Parse query result...', 'yellow', end='\n\n')
                data = None
                columns: list = _get_column_names(cursor=self.cursor)
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
        self.cursor.execute(sql, args)
        colored_print(f'Sending {type.upper()} query to MySQL...', 'yellow')
        try:
            if type == 'select':
                result: list = list(self.cursor.fetchall())
                columns: list = _get_column_names(cursor=self.cursor)
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
    db.send_query(sql=sql, type='select', save='yaml')
    db.close_DB_session()
