from timo.file_manager.file_reader import Reader
from timo.utils import colored_print
from timo.utils import equals
import re


class ESLintParser(object):
    def __init__(self):
        self.reader = Reader()

    def parse(self, path: str, file_type: str) -> dict:
        def _checkstyle() -> dict:
            def find_warnings(file_tag: dict):
                if 'error' not in file_tag:
                    return 0
                if isinstance(file_tag['error'], list):
                    return len(file_tag['error'])
                return 1
            xml = self.reader.read_xml_file(path)
            data = xml['checkstyle']['file']
            warnings = 0
            if isinstance(data, list):
                for tag in data:
                    warnings += find_warnings(tag)
            else:
                warnings = find_warnings(data)
            return {
                'warning': warnings
            }

        def _codeframe() -> dict:
            txt = self.reader.read_raw_file(path)
            result_line = txt.splitlines()[-2]
            result = re.sub('[^0-9]', '', result_line)
            return {
                'warning': int(result[0]) + int(result[1])
            }

        def _compact() -> dict:
            txt = self.reader.read_raw_file(path)
            result_line = txt.splitlines()[-1]
            return {
                'warning': int(result_line.split()[0])
            }

        def _junit() -> dict:
            xml = self.reader.read_xml_file(path)
            return {
                'warning': int(xml['testsuites']['testsuite']['@errors'])
            }

        def _jslint_xml() -> dict:
            xml = self.reader.read_xml_file(path)
            return {
                'warning': len(xml['jslint']['file']['issue'])
            }

        def _json() -> dict:
            json = self.reader.read_json_file(path)
            warning = int(json[0]['errorCount']) + int(json[0]['warningCount'])
            return {
                'warning': warning
            }

        def _json_with_metadata() -> dict:
            json = self.reader.read_json_file(path)
            warning = int(json['results'][0]['errorCount']) + int(json['results'][0]['warningCount'])
            return {
                'warning': warning
            }

        if equals(file_type, 'checkstyle'):
            return _checkstyle()
        if equals(file_type, 'codeframe'):
            return _codeframe()
        if equals(file_type, 'compact'):
            return _compact()
        if equals(file_type, 'junit'):
            return _junit()
        if equals(file_type, 'jslint-xml'):
            return _jslint_xml()
        if equals(file_type, 'json'):
            return _json()
        if equals(file_type, 'json-with-metadata'):
            return _json_with_metadata()

        colored_print('Sorry, there is no information you can get from this type of file.', 'orange')
