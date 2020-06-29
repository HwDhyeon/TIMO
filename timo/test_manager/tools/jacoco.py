""""""

from file_manager.file_reader import Reader
from utils import colored_print


class JacocoParser(object):
    def __init__(self):
        self.reader = Reader()

    def parse(self, path: str, file_type: str) -> {str, int}:
        return_val = {'test_tool': 'jacoco', 'test_val': 0}
        if file_type == 'html':
            html = self.reader.read_html_file(path)
            return_val['test_val'] = int(html['html']['body']['table']['tfoot']['tr']['td'][2]['text'].rstrip('%'))
        elif file_type == 'csv':
            # csv = self.reader.read_raw_file(path)
            colored_print('Sorry, there is no information you can get from this type of file.', 'orange')
            return_val['test_val'] = -1
        elif file_type == 'xml':
            # xml = self.reader.read_xml_file(path)
            return_val['test_val'] = -1
        
        return return_val
