from timo.file_manager.file_reader import Reader
from timo.utils import colored_print


class Flake8Parser(object):
    def __init__(self):
        self.reader = Reader()

    def parse(self, path: str, file_type: str) -> dict:
        return_val = {'warning': 0}
        if file_type == 'txt':
            test_result = self.reader.read_raw_file(path)
            return_val['warning'] = len(test_result.split('\n')) - 1
        else:
            colored_print('Sorry, there is no information you can get from this type of file.', 'orange')

        return return_val
