from timo.command_manager.test_runner import TestRunner
from timo.file_manager.config_reader import ConfigReader
from typing import NoReturn
import fire


class Main(object):
    def __init__(self):
        self.conf = ConfigReader('foo')
    def run(self, test_name: str) -> NoReturn:
        # test_kinds = ['CSW', 'Unittest', 'Coverage', 'APItest', 'E2Etest']
        print(f'Running {test_name} in now.')


class AfterTest(object):
    pass


if __name__ == "__main__":
    fire.Fire({
        'run test': print('SS')
    })
