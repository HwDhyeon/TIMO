from timo.file_manager.file_reader import Reader
from typing import Dict
from typing import List


class ConfigReader(object):
    def __init__(self, project_name: str):
        self._file_reader: Reader = Reader()
        self._project_name: str = project_name

    def read_config_file(self, path: str) -> Dict:
        self.conf = self._file_reader.read_yaml_file(f'data/{self._project_name}.conf.yaml')
        return self.conf

    def get_project_name(self) -> str:
        return self.conf['project-name']

    def get_project_version(self) -> str:
        return self.conf['version']

    def get_tests(self) -> List[str]:
        return [*self.conf['Tests']]
    
    def get_test_suites(self, test_name) -> List[str]:
        return self.conf['Tests'][test_name]['run']

    def get_report_info(self, test_name) -> Dict:
        return self.conf['Tests'][test_name]['report']

    def get_score_info(self) -> Dict:
        if self.conf['Score']['custom'] == 'False':
            return {
                'CSW': '20%',
                'Unittest': '20%',
                'Coverage': '20%',
                'APItest': '20%',
                'E2Etest': '20%'
            }
        else:
            return self.conf['Score']['set']

    def get_post_info(self) -> Dict[str, Dict]:
        return {
            'type': self.conf['Post']['type'],
            'info': self.conf['Post']['set']
        }


if __name__ == "__main__":
    import sys
    sys.path.append("..")
    sys.path.append(".")
    rr = ConfigReader('foo')
    print(rr.get_tests())
