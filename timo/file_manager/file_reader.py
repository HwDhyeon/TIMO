"""Read various files."""

from bs2json import bs2json
from bs4 import BeautifulSoup  # HTML 파싱 모듈
from exception import FileExtensionError
from typing import Dict
from typing import NoReturn
import xmltodict  # XML 파싱 모듈
import json
import yaml


class Reader(object):
    """파일내용을 규칙에 따라 읽습니다."""

    def _check_file_extension(self, path: str, ext: str) -> NoReturn:
        """
        Checks whether the extension of the file matches the requirements.

            Parameters:
                path(str): Path to the file
                ext(srt): Required file extension

            Raised:
                FileExtensionError: If the file extensions do not match, an appropriate error is generated.
        """

        file_ext = path.split('.')[-1]
        if file_ext != ext:
            raise FileExtensionError

    def read_raw_file(self, path: str) -> str:
        """
        Reads any file and returns it as a string.

            Parameters:
                path(str): Path to the file

            Returns:
                str: String containing the contents of the file
        """

        with open(file=path, mode='r', encoding='utf-8') as f:
            return f.read()

    def read_html_file(self, path: str) -> Dict:
        """
        Read an HTML file and return the result as a Dictionary.

            Parameters:
                path(str): Path to the file

            Returns:
                dict: Dictionary containing HTML element structure
        """

        self._check_file_extension(path, 'html')
        html_string: str = self.read_raw_file(path)
        soup: BeautifulSoup = BeautifulSoup(html_string, 'html.parser')
        converter: bs2json = bs2json()  # HTML을 dict로 변환하기 위한 모듈
        tag = soup.find('html')  # 최상단 엘리먼트인 html 태그를 찾는다
        json_html: dict = converter.convert(tag)  # html 태그를 포함하여 하위의 모든 태그와 속성을 dict로 변환한다
        return json_html  # 변환된 HTML을 리턴한다

    def read_xml_file(self, path: str) -> Dict:
        """
        Read an XML file and return the result as a Dictionary.

            Parameters:
                path(str): Path to the file

            Returns:
                dict: Dictionary containing XML element structure
        """

        self._check_file_extension(path, 'xml')
        xml_string: str = self.read_raw_file(path)
        xml_dict = xmltodict.parse(xml_string)
        xml_json = json.dumps(xml_dict)
        xml_dict = json.loads(xml_json)
        return xml_dict

    def read_json_file(self, path: str) -> Dict:
        """
        Read an JSON file and return the result as a Dictionary.

            Parameters:
                path(str): Path to the file

            Returns:
                dict: Dictionary containing JSON element structure
        """

        self._check_file_extension(path, 'json')
        json_string: str = self.read_raw_file(path)
        json_data: dict = json.loads(json_string)
        return json_data

    def read_yaml_file(self, path: str) -> Dict:
        """
        Read an YAML file and return the result as a Dictionary.

            Parameters:
                path(str): Path to the file

            Returns:
                dict: Dictionary containing YAML element structure
        """

        ext = path.split('.')[-1]
        if ext != 'yml' and ext != 'yaml':
            ext = 'yaml'
        self._check_file_extension(path, ext)
        yaml_string: str = self.read_raw_file(path)
        yaml_data: dict = yaml.safe_load(yaml_string)
        return yaml_data

    def read_yml_file(self, path: str) -> Dict:
        """
        Read an YML file and return the result as a Dictionary.

            Parameters:
                path(str): Path to the file

            Returns:
                dict: Dictionary containing YML element structure
        """

        return self.read_yaml_file(path)
