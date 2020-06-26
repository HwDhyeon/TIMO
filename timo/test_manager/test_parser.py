from file_manager.file_reader import Reader
from test_manager.tools.jacoco import JacocoParser
from test_manager.tools.surefire import SurefireParser
from test_manager.tools.unittest import UnittestParser
from typing import NoReturn
from typing import Union


class Parser(object):
    def __init__(self) -> NoReturn:
        self.reader: Reader = Reader()
        self.surefire = SurefireParser()
        self.unittest = UnittestParser()
        self.jacoco = JacocoParser()

    def _set_result_dict(self, success, fail, skip):
            self.return_value['success'] = str(success)
            self.return_value['fail'] = str(fail)
            self.return_value['skip'] = str(skip)

    def _csw(self) -> NoReturn:
        pass

    def _unittest(self) -> NoReturn:
        if self.test_tool == 'surefire':
            result: str = self.reader.read_raw_file(self.path).split('\n')[-1].split(', ')
            total = int(result[0].split()[-1])
            fail = int(result[1].split()[-1])
            skip = int(result[2].split()[-1])
            success: int = total - fail - skip
            self._set_result_dict(success, fail, skip)

    def _coverage(self) -> NoReturn:
        pass

    def _apitest(self) -> NoReturn:
        pass

    def _e2etest(self) -> NoReturn:
        pass

    def parse(self, kind: Union['CSW', 'Unittest', 'Coverage', 'APItest', 'E2Etest'], report_path: str, test_tool: str):
        self.path = report_path
        self.test_tool = test_tool
        self.return_value = { 'tool': self.test_tool, 'success': '', 'fail': '', 'skip': '' }
        if (kind := kind.upper()) == 'CSW':
            self._csw()
        elif kind == 'UNITTEST':
            self._unittest()
        return self.return_value


if __name__ == "__main__":
    p = Parser()
    print(p.parse('unittest', './s.txt', 'surefire'))
