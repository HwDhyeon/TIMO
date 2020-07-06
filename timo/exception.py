from typing import AnyStr
from typing import NoReturn


class Error(Exception):
    """
    This is the basis of all errors.\n
    Basically the same as Exception.
    """

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


class UnknownDataError(Error):
    """This error occurs when data cannot be found."""

    def __str__(self) -> str:
        return '찾을 수 없거나 잘못된 데이터입니다.'


class UnknownDatabaseError(Error):
    """This error occurs when the database cannot be found."""

    def __str__(self) -> str:
        return '찾을 수 없거나 존재하지 않는 데이터베이스입니다.'
