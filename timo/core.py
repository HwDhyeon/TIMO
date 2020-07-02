from database_manager.mysql import MySQL
from file_manager.config_reader import ConfigReader
from test_manager.command_runner import CommandRunner
from test_manager.result_parser import Parser
from typing import NoReturn
from utils import colored_print
from utils import pretty_print
import fire


class Main(object):
    def __init__(self):
        self.conf = ConfigReader()
        self.runner = CommandRunner()

    def run(self, test_name: str) -> NoReturn:
        # test_kinds = ['CSW', 'Unittest', 'Coverage', 'APItest', 'E2Etest']
        colored_print(f'Running {test_name} in now.', 'magenta')
        command_list = self.conf.get_test_suites(test_name)
        self.runner.run_all(command_list)


class AfterTest(object):
    def __init__(self):
        self.mysql = MySQL()
        self.conf = ConfigReader()
        self.parser = Parser()

    def _create_query(self, test_name: str) -> str:
        return_string = ''
        test_name = test_name.lower()
        if test_name == 'csw':
            return_string = ''
        elif test_name == 'unittest':
            return_string = 'INSERT INTO UNITTEST(PROJECT_NAME, BUILD_NUMBER, TEST_TOOL, SUCCESS, FAIL, SKIP) VALUES(\'IRIS-E2E\', )'
        elif test_name == 'apitest':
            pass
        elif test_name == 'e2etest':
            pass

        return return_string

    def parse_test_result(self, test_name) -> dict:
        file_type = self.conf.get_report_info(test_name)['type']
        test_tool = self.conf.get_test_tool(test_name)['uses']
        result = self.parser.parse(kind=test_name, file_type=file_type, test_tool=test_tool)
        pretty_print(result)
        return result


class Pipeline(object):
    def __init__(self):
        self.conf = ConfigReader()
        self.test = Main()
        self.after_test = AfterTest()

    def setting(self, ext):
        self.conf.read_config_file(ext)

    def run(self, test_name):
        self.test.run(test_name)

    def parse(self, test_name, db=False):
        result = self.after_test.parse_test_result(test_name)
        if db:
            pass


if __name__ == "__main__":
    fire.Fire(Pipeline)
