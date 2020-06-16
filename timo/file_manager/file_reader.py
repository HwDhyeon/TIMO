from bs4 import BeautifulSoup # HTML 파싱 모듈
from typing import Dict
from typing import NoReturn
import xml.etree.ElementTree as ElementTree # XML 파싱 모듈
import json
import yaml

class Reader(object):
    def read_raw_file(self, path) -> str:
        with open(file=path, mode='r', encoding='utf-8') as f:
            return f.read()

    def read_html_file(self, path: str):
        html_string: str = self.read_raw_file(path)
        return html_string

    def read_xml_file(self, path: str):
        xml_string: str = self.read_raw_file(path)
        return xml_string

    def read_json_file(self, path: str) -> Dict:
        json_string: str = self.read_raw_file(path)
        json_data: dict = json.loads(json_string)
        return json_data

    def read_yaml_file(self, path: str) -> Dict:
        yaml_string: str = self.read_raw_file(path)
        yaml_data: dict = yaml.safe_load(yaml_string)
        return yaml_data


if __name__ == "__main__":
    r = Reader()
    rr = r.read_json_file('sql.json')
    print(rr)
    rr = r.read_yaml_file('sql.yaml')
    print(rr)
