from database_manager.databases import mariadb
from database_manager.databases import mongodb
from database_manager.databases import mysql
from database_manager.databases import oracle
from exception import UnknownDataError
from exception import UnknownDatabaseError
from file_manager.config_reader import ConfigReader
from file_manager.file_reader import Reader
from typing import NoReturn
from utils import colored_print
from utils import equals
import os


class DatabaseManager(object):
    """Everything that happens in the database is done through this class."""

    def __init__(self):
        self.config = ConfigReader()
        self.mariadb = mariadb.MariaDB()
        self.mongodb = mongodb.MongoDB()
        self.mysql = mysql.MySQL()
        self.oracle = oracle.Oracle()
        self.reader = Reader()

    def _create_new_query(self, test_name: str, data: dict) -> str:
        """
        Generates SQL query statement containing each test result.

            Parameters:
                test_name(str): Name of the test performed.
                data(dict): This is a dictionary containing test results.

            Returns:
                str: Generated SQL query statement.
        """        

        test_name = test_name.lower()
        project_name = self.config.get_project_name()
        test_tool = self.config.get_test_tool(test_name=test_name.upper())
        if equals(test_name, 'csw'):
            return f"INSERT INTO CSW(PROJECT_NAME, BUILD_NUMBER, TEST_TOOL, TEST_VAL) VALUES('{project_name}', {data['build_number']}, '{test_tool['uses']}', {data['warning']})"
        elif equals(test_name, 'unittest'):
            return f"""INSERT
            INTO
                UNITTEST(PROJECT_NAME, BUILD_NUMBER, TEST_TOOL, SUCCESS, FAIL, SKIP)
            VALUES
                ('{project_name}', {data['build_number']}, '{test_tool['uses']}', {data['success']}, {data['fail']}, {data['skip']})"""
        elif equals(test_name, 'coverage'):
            return f"""INSERT
            INTO
                COVERAGE(PROJECT_NAME, BUILD_NUMBER, TEST_TOOL, TEST_VAL)
            VALUES
                ('{project_name}', {data['build_number']}, '{test_tool['uses']}', {data['test_val']})
            """
        elif equals(test_name, 'apitest'):
            pass
        elif equals(test_name, 'e2etest'):
            pass

    def insert_test_result(self, test_name: str, data: dict, db_name: str) -> NoReturn:
        """
        The test results are analyzed and inserted into the database.\n
        Tables must be prepared for each test name.\n
        Example: CSW, UNITTEST, E2ETEST

            Parameters:
                test_name(str): Name of the test performed.
                data(dict): This is a dictionary containing test results.
                db_name(str): Database type name.
                              Examples: MySQL, Oracle, MongoDB, MariaDB...
        """

        if not os.path.isfile('data/db.json'):  # db.json 파일이 없을경우 오류 발생
            raise FileNotFoundError
        else:
            db_data = self.reader.read_json_file('data/db.json')

        if db_name in list(db_data):  # 입력받은 데이터베이스가 목록에 없을 경우 오류 발생
            if equals(db_name, 'mariadb'):
                colored_print('Currently MariaDB is handled as MySQL.', 'orange')
                self.insert_test_result(test_name=test_name, data=data, db_name='mysql')
            elif equals(db_name, 'mongodb'):
                colored_print('Database type not currently supported.', 'orange')
            elif equals(db_name, 'mysql'):
                self.mysql.open_DB_session()
                self.mysql.send_query(sql=self._create_new_query(test_name, data), type='insert')
                self.mysql.close_DB_session()
            elif equals(db_name, 'oracle'):
                colored_print('Database type not currently supported.', 'orange')
            else:
                colored_print('Database type not currently supported.', 'orange')
                raise UnknownDatabaseError  # 목록에는 있지만 지원하지 않는 데이터베이스의 경우 오류 발생
        else:
            raise UnknownDataError
