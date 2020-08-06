"""
Parse the results of tests conducted with the surefire plugin.

http://maven.apache.org/surefire/maven-surefire-plugin/
"""

from timo.file_manager.file_reader import Reader
from typing import Dict
from typing import NoReturn
from timo.utils import colored_print
import glob


class SurefireParser(object):
    """Read result file of surefire execution."""

    def __init__(self) -> NoReturn:
        self.reader: Reader = Reader()  # 결과 파일을 읽기위해 클래스 선언

    def parse(self, path: str, file_type: str) -> Dict:
        """
        Read the surefire test result file, find the failure and skip values, and use it to find the success value and create a dictionary.

            Parameters:
                path(str): Report file path

            Returns:
                dict: This is a dictionary containing test results.
        """

        return_val: dict = {
            'success': 0,
            'fail': 0,
            'skip': 0
        }  # 반환할 값 미리 세팅 file_type이 맞지 않을 경우 이 값을 반환한다
        for test in glob.glob(pathname=path + "/TEST*.xml"):
            if file_type == 'xml':
                xml: dict = self.reader.read_xml_file(test)
                data: dict = xml['testsuite']
                return_val['fail'] += int(data['@failures']) + int(data['@errors'])  # 에러 개수와 실패 개수를 모두 실패 개수로 판단
                return_val['skip'] += int(data['@skipped'])  # 스킵된 테스트 개수
                return_val['success'] += int(data['@tests']) - return_val['fail'] - return_val['skip']
            elif file_type == 'txt':
                colored_print('Warning:', 'red')
                colored_print('\tThis feature is still incomplete.', 'red')
                colored_print('\tAn error may occur.', 'red')
                text: str = self.reader.read_raw_file(test)
                result_line: list = []
                for line in text[-1].split(', '):
                    if 'Tests run:' in line:
                        result_line.append(line)
                total: str = int(result_line[0].split()[-1])  # 전체 테스트 개수
                return_val['fail'] += int(result_line[1].split()[-1]) + int(result_line[2].split()[-1])  # 에러 개수와 실패 개수를 모두 실패 개수로 판단
                return_val['skip'] += int(result_line[3].split()[-1])  # 스킵된 테스트 개수
                return_val['success'] += total - return_val['fail'] - return_val['skip']
        return return_val
