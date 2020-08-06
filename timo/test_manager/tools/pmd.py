from timo.file_manager.file_reader import Reader
from timo.utils import colored_print
from timo.utils import equals
from timo.exception import FileExtensionError


class PMDParser(object):
    def __init__(self):
        self.reader = Reader()

    def parse(self, path: str, file_type: str) -> dict:
        return_val = {'warning': 0}
        try:
            if not equals(file_type, 'xml'):
                raise FileExtensionError
            test_result = self.reader.read_xml_file(path)
            data = test_result['pmd']['file']
        except FileExtensionError:
            colored_print('Sorry, there is no information you can get from this type of file.', 'orange')
        except ValueError:
            pass
        else:
            if equals(isinstance(data, dict), True):
                data = [data]
            for file in data:
                if 'violation' in file:
                    if equals(isinstance(file['violation'], dict), True):
                        file['violation'] = [file['violation']]
                    return_val['warning'] += len(file['violation'])
        finally:
            return return_val
