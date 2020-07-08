from file_manager.file_reader import Reader
from utils import colored_print
from utils import equals


class CoverageParser(object):
    def __init__(self):
        self.reader = Reader()

    def parse(self, path: str, file_type: str) -> dict:
        return_val = { 'test_val': 0 }
        if equals(file_type, 'html'):
            coverage_data = self.reader.read_html_file(path)
            rate = int(coverage_data['html']['body']['div'][2]['table']['tfoot']['tr']['td'][4]['text'].rstrip('%'))
            return_val['test_val'] = rate
        elif equals(file_type, 'xml'):
            coverage_data = self.reader.read_xml_file(path)
            rate = coverage_data['coverage']['@line-rate'].split('.')[1][:2]
            return_val['test_val'] = int(rate)
        elif equals(file_type, 'json'):
            coverage_data = self.reader.read_json_file(path)
            return_val['test_val'] = int(coverage_data['totals']['percent_covered'])
        else:
            colored_print('Sorry, there is no information you can get from this type of file.', 'orange')
            return_val['test_val'] = -1

        return return_val


if __name__ == "__main__":
    c = CoverageParser()
    print(c.parse('coverage.json', 'json'))
    print(c.parse('coverage.xml', 'xml'))
    print(c.parse('htmlcov/index.html', 'html'))
