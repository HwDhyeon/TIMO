from typing import AnyStr
from typing import NoReturn

class Error(Exception):
    def __init__(self, msg: AnyStr) -> NoReturn:
        self.msg: str = msg

    def __str__(self) -> str:
        return self.msg


class FileExtensionError(Error):
    """This error occurs when the file extension does not meet the requirements."""

    def __str__(self) -> str:
        return '파일 확장명이 올바르지 않습니다.'


class UnknownTestTestToolError(Error):
    """This error is caused when an invalid test tool is entered."""

    def __str__(self) -> str:
        return '현재 지원하지 않거나 잘못된 테스트 도구입니다.'
