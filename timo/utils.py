"""Functions used repeatedly to improve the convenience and readability of source code are described here."""

from colors import color
from typing import Any
from typing import AnyStr
from typing import List
from typing import NoReturn


def colored_print(msg: Any, colorname: str, end='\n') -> NoReturn:
    """
    Apply color to the print function.

        Parameters:
            msg (str):        Message to print
            color_name (str): Color
            end (str) :       Same as end parameter of print function
    """

    print(color(msg, colorname), end=end)


def pretty_print(obj: Any) -> NoReturn:
    """
    The object is processed according to the format and output.

        Parameters:
            obj(any): Any
    """

    def _print():
        for key, value in obj.items():
            print('│' + '―' * 15 + '┼' + '―' * 15 + '│')
            print('│{key:^15}│{value:^15}│'.format(key=key, value=value))
        print('└' + '―' * 15 + '┴' + '―' * 15 + '┘')

    if equals(type(obj), dict, deep=True):
        print('┌' + '―' * 15 + '┬' + '―' * 15 + '┐')
        print('│      key      │     value     │')
        _print()
    elif equals(type(obj), list, deep=True) or equals(type(obj), tuple, deep=True) or equals(type(obj), set, deep=True):
        obj = dict(zip([x for x in range(len(obj))], obj))
        print('┌' + '―' * 15 + '┬' + '―' * 15 + '┐')
        print('│     index     │     value     │')
        _print()


def get_command_black_list() -> List[AnyStr]:
    """
    Get a list of commands to exclude from execution.

        Returns:
            list[str]: List of commands to exclude from execution.
    """

    return ['', 'dir']


def equals(obj1, obj2, *, deep=False) -> bool:
    """
    Checks whether two input objects are the same and returns the result in Boolean.

        Parameters:
            obj1(object): Objects to compare for equality.
            obj2(object): Objects to compare for equality.
            deep(bool): Specifies the scope of the comparison.
                        The default value is false, and if true, compares two objects for equality,
                        and if false, compares the values of two objects for equality.

        Returns:
            bool: The comparison value of two objects.
    """

    if not deep:
        return True if obj1 == obj2 else False
    else:
        return True if obj1 is obj2 else False


if __name__ == "__main__":
    pretty_print({'a': '1', 'b': '2', 'cdsmfefuiguh': 12348234723})
    pretty_print([1111, 2434, 443, 43244, 235, 612233, 'asdjksdjfyj'])
    pretty_print((1111, 2434, 443, 43244, 235, 612233, 'asdjksdjfyj'))
    pretty_print({1111, 2434, 443, 43244, 235, 612233, 'asdjksdjfyj'})
