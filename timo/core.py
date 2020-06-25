from database_manager.mysql import MySQL
from file_manager.config_reader import ConfigReader
from test_manager.test_runner import TestRunner
from typing import NoReturn
from utils import colored_print
import fire


class Main(object):
    def __init__(self):
        self.conf = ConfigReader()
        self.runner = TestRunner()

    def run(self, test_name) -> NoReturn:
        # test_kinds = ['CSW', 'Unittest', 'Coverage', 'APItest', 'E2Etest']
        colored_print(f'Running {test_name} in now.', 'magenta')
        command_list = self.conf.get_test_suites(test_name)
        self.runner.run_all(command_list)


class AfterTest(object):
    pass


class Pipeline(object):
    def __init__(self):
        self.test = Main()
        self.conf = ConfigReader()

    def run(self, test_name):
        self.test.run(test_name)

    def setting(self, ext):
        self.conf.read_config_file(ext)



if __name__ == "__main__":
    fire.Fire(Pipeline)
