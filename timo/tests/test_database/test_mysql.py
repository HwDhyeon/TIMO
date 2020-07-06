from database_manager.mysql import MySQL
import unittest
import json
import os


class TestMySQL(unittest.TestCase):
    def setUp(self):
        self.db = MySQL()
        self.db.open_DB_session()

    def tearDown(self):
        self.db.close_DB_session()

    def test_select_query_print(self):
        self.db.send_query(sql="SELECT MAX(BUILD_NO) FROM JENKINS_BUILD_RESULT WHERE PROJECT_NM = 'IRIS-E2E-SAAS'", type='select', save=None)

    def test_select_query_save_json(self):
        self.db.send_query(sql="SELECT MAX(BUILD_NO) FROM JENKINS_BUILD_RESULT WHERE PROJECT_NM = 'IRIS-E2E-SAAS'", type='select', save='json')
        assert os.path.isfile(os.getcwd() + '/out.json')
        with open(file=os.getcwd() + '/out.json', mode='r', encoding='utf-8') as f:
            data = json.load(f)
        assert len(data) == 1
        assert type(data[0]['MAX(BUILD_NO)']) is int


if __name__ == "__main__":
    unittest.main()
