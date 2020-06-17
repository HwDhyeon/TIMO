from typing import AnyStr
from typing import NoReturn

class Error(Exception):
    def __init__(self, msg: AnyStr) -> NoReturn:
        self.msg: str = msg

    def __str__(self) -> str:
        return self.msg


class FileExtensionError(Error):
    def __str__(self) -> str:
        return '파일 확장명이 올바르지 않습니다.'
