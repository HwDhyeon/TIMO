# -*- coding: utf-8 -*-

from colors import color
from timo.database_manager.database import DatabaseManager
from timo.file_manager.config_reader import ConfigReader
from timo.score_manager.score_manager import ScoreCalculator
from timo.test_manager.command_runner import CommandRunner
from timo.test_manager.result_parser import Parser
from typing import NoReturn
from typing import Union
from timo.utils import colored_print
from timo.utils import pretty_print
import fire


class Main(object):
    def __init__(self):
        self.conf = ConfigReader()
        self.runner = CommandRunner()

    def run(self, test_name: str) -> NoReturn:
        """
        Execute the command.

            Parameters:
                test_name(str): Name of the test to run.
        """

        # test_kinds = ['CSW', 'Unittest', 'Coverage', 'APItest', 'E2Etest']
        colored_print(f'Running {test_name} in now. 🚀', 'magenta')
        command_list = self.conf.get_test_suites(test_name)
        self.runner.run_all(command_list)


class AfterTest(object):
    def __init__(self):
        self.config = ConfigReader()
        self.db = DatabaseManager()
        self.parser = Parser()
        self.score = ScoreCalculator()

    def parse(self, test_name: str, db: str, build_number: int) -> NoReturn:
        """
        Parse test results.

            Parameters:
                test_name(str): The name of the test for which you want to parse the results.
                db(str): This is the type of database if you want to store the results in a database.
                build_number(int): Jenkins build number if you want to store the results in a database.
        """

        report_conf = self.config.get_report_info(test_name=test_name)
        test_tool = self.config.get_test_tool(test_name=test_name)
        test_result = self.parser.parse(kind=test_name, file_type=report_conf['type'], test_tool=test_tool['uses'])
        if db is not None and build_number is not None:
            test_result['build_number'] = build_number
            self.db.insert_test_result(
                test_name,
                test_result,
                db
            )
        else:
            pretty_print(test_result)


class Pipeline(object):
    def __init__(self):
        self.conf = ConfigReader()
        self.test = Main()
        self.after_test = AfterTest()

    def setting(self, ext: str) -> NoReturn:
        """
        Set the configuration file to be used.

            Parameters:
                ext(str): File extension.
                          Supported forms are available at: https://github.com/HwDhyeon/TIMO#setting
        """

        self.conf.read_config_file(ext)

    def get(self, option: str) -> Union[str, NoReturn]:
        """
        This is used when you want to see various information in the configuration file or the score of the entire test.

            Parameters:
                option(str): This is the information you want to view.

            Returns:
                Union(str, NoReturn): It can return a string or nothing.
        """

        if (option := option.lower()) == 'name':
            return "Project name: " + color(self.conf.get_project_name(), 'green')
        elif option == 'version':
            return ("Project version: %s\nTIMO version: %s"
                    % (color(self.conf.get_project_version(), 'green'), color('alpha', 'orange')))
        elif option == 'score':
            self.after_test.score.calculate()

    def run(self, test_name: str) -> NoReturn:
        """
        Perform tests.

            Parameters:
                test_name(str): Name of the test to run.
        """

        self.test.run(test_name)

    def parse(self, test_name: str, db=None, build_number=None) -> NoReturn:
        """
        Parse test results.

            Parameters:
                test_name(str): The name of the test for which you want to parse the results.
                db(str): This is the type of database if you want to store the results in a database.
                build_number(int): Jenkins build number if you want to store the results in a database.
        """

        self.after_test.parse(test_name=test_name, db=db, build_number=build_number)


if __name__ == "__main__":
    fire.Fire(Pipeline)
