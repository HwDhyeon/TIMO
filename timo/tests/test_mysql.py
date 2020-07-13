from database_manager.databases.mysql import MySQL
import HtmlTestRunner
import xmlrunner
import unittest
import json
import os
import yaml


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
        os.remove(os.getcwd() + '/out.json')

    def test_select_query_save_yaml(self):
        self.db.send_query(sql="SELECT MAX(BUILD_NO) FROM JENKINS_BUILD_RESULT WHERE PROJECT_NM = 'IRIS-E2E-SAAS'", type='select', save='yaml')
        assert os.path.isfile(os.getcwd() + '/out.yaml')
        with open(file=os.getcwd() + '/out.yaml', mode='r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        assert len(data) == 1
        assert type(data[0]['MAX(BUILD_NO)']) is int
        os.remove(os.getcwd() + '/out.yaml')

    def test_select_query_save_yml(self):
        self.db.send_query(sql="SELECT MAX(BUILD_NO) FROM JENKINS_BUILD_RESULT WHERE PROJECT_NM = 'IRIS-E2E-SAAS'", type='select', save='yml')
        assert os.path.isfile(os.getcwd() + '/out.yml')
        with open(file=os.getcwd() + '/out.yml', mode='r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        assert len(data) == 1
        assert type(data[0]['MAX(BUILD_NO)']) is int
        os.remove(os.getcwd() + '/out.yml')


if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='unittest-report'))
    #  with open(file='unittest-xml-report.xml', mode='wb') as output:
    #     unittest.main(
    #         testRunner=xmlrunner.XMLTestRunner(output=output),
    #         failfast=False, buffer=False, catchbreak=False
    #     )
