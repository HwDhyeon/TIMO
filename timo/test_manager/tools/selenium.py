from timo.file_manager.file_reader import Reader
from timo.utils import colored_print


class SeleniumParser(object):
    def __init__(self):
        self.reader = Reader()

    def parse(self, path: str, file_type: str) -> dict:
        return_val: dict = {
            'success': 0,
            'fail': 0,
            'skip': 0
        }
        if file_type == 'xml':
            selenium_data = self.reader.read_xml_file(path)
            total = int(selenium_data['testsuites']['@tests'])
            fail = int(selenium_data['testsuites']['@failures'])
            success = total - fail
            return_val['success'] = success
            return_val['fail'] = fail
        else:
            colored_print('Sorry, there is no information you can get from this type of file.', 'orange')

        return return_val
