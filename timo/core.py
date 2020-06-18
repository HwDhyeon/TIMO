from command_manager.test_runner import TestRunner
from file_manager.config_reader import ConfigReader
from typing import NoReturn
import fire


class Main(object):
    def __init__(self):
        self.conf = ConfigReader('foo')
    def run(self, test_name=None) -> NoReturn:
        # test_kinds = ['CSW', 'Unittest', 'Coverage', 'APItest', 'E2Etest']
        print(f'Running {test_name} in now.')


class AfterTest(object):
    pass


class Pipeline(object):
    def __init__(self):
        self.test = Main()

    def run(self):
        self.test.run()


if __name__ == "__main__":
    fire.Fire(Pipeline)
