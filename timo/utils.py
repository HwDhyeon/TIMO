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


def get_command_black_list() -> List[AnyStr]:
    """
    Get a list of commands to exclude from execution.

        Returns:
            list[str]: List of commands to exclude from execution.
    """

    return ['dir',]


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
