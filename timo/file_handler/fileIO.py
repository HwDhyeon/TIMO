from typing import Union
from timo.file_handler import file_reader
from timo.file_handler import file_writer


class File_IO_Tool(object):
    def __init__(self):
        pass

    def read_file(self, path: str) -> Union[str, dict]:
        ext = path.split('.')[:-1]
        if ext == 'json':
            return file_reader.read_json_file(path)
        elif ext == 'yaml':
            return file_reader.read_yaml_file(path)
        elif ext == 'html':
            return file_reader.read_html_file(path)
        elif ext == 'xml':
            return file_reader.read_xml_file(path)
        else:
            return file_reader.read_raw_file(path)
