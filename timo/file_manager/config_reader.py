"""Read and interpret the project configuration file."""

from file_manager.file_reader import Reader
from file_manager.file_writer import Writer
from exception import FileExtensionError
from typing import Dict
from typing import List
from typing import NoReturn
from utils import colored_print
import os


class ConfigReader(object):
    """This class loads various settings."""

    def __init__(self) -> NoReturn:
        self._file_reader: Reader = Reader()
        self._file_writer: Writer = Writer()

    def read_config_file(self, ext=None, confpath='data/configpath.json') -> Dict:
        """
        Read the project configuration file.

            Returns:
                dict: A dictionary containing all the information in the configuration file
        """

        def _read_config(ext: str) -> Dict:
            if ext == 'json' and os.path.isfile('data/conf.json'):
                path = 'data/conf.json'
                conf = self._file_reader.read_json_file(path)
            elif (ext == 'yaml' or ext == 'yml') and os.path.isfile(f'data/conf.{ext}'):
                path = f'data/conf.{ext}'
                conf = self._file_reader.read_yaml_file(path)
            else:
                raise FileExtensionError
            return conf

        if ext is not None:
            if ext not in ['json', 'yaml', 'yml']:
                raise FileExtensionError
            else:
                colored_print('We found new configuration file.', 'cyan')
            self._file_writer.write_file('data/configpath.json', {'ConfType': ext}, 'json')
            return _read_config(ext)
        else:
            if confpath is not None:
                ext = self._file_reader.read_json_file('data/configpath.json')['ConfType']
                return _read_config(ext)
            else:
                raise FileNotFoundError

    def get_project_name(self) -> str:
        """
        Find the name of your project.  
        If the project name in the configuration file and the name of the configuration file are different, the project name in the configuration file is returned.

            Returns:
                str: The name of the project
        """
        return self.read_config_file()['project-name']

    def get_project_version(self) -> str:
        """
        Returns the version of the project.

            Returns:
                str: Project version
        """
        return self.read_config_file()['version']

    def get_tests(self) -> List[str]:
        """
        Returns the type of all tests declared in the file.

            Returns:
                list[str]: List of strings containing test types
        """
        return [*self.read_config_file()['Tests']]
    
    def get_test_suites(self, test_name: str) -> List[str]:
        """
        Returns the statement of a specific test.

            Parameters:
                test_name(str): Test name

            Returns:
                list[str]: List of string-type statements
        """
        return self.read_config_file()['Tests'][test_name]['run']

    def get_report_info(self, test_name: str) -> Dict:
        """
        Returns the definition of processing results for a particular test.

            Parameters:
                test_name(str): Test name

            Returns:
                dict: Dictionary with report information
        """
        return self.read_config_file()['Tests'][test_name]['report']

    def get_test_tool(self, test_name: str) -> Dict:
        return {
            'uses': self.read_config_file()['Tests'][test_name]['uses']
        }

    def get_score_info(self) -> Dict:
        """
        Returns the overall score processing percentage of the build.
        If custom item is False, default value is returned.

            Returns:
                dict: A dictionary containing information on the score ratio for each test
        """
        if self.read_config_file()['Score']['custom'] == 'False':
            return {
                'CSW': '20%',
                'Unittest': '20%',
                'Coverage': '20%',
                'APItest': '20%',
                'E2Etest': '20%'
            }
        else:
            return self.read_config_file()['Score']['set']

    def get_post_info(self) -> Dict[str, Dict]:
        """
        Returns information about where to send build results.

            Returns:
                dict{ str, dict }: Dictionary of post format and destination
        """
        return {
            'type': self.read_config_file()['Post']['type'],
            'info': self.read_config_file()['Post']['set']
        }
