from decorators import timer
from utils import colored_print
from utils import equals
from utils import get_command_black_list
from typing import List
from typing import NoReturn
import platform
import subprocess
import shlex


class CommandRunner(object):
    """Perform tests."""

    def _convert_byte_to_string(self, byte_string: str) -> str:
        """
        Decodes Byte format strings and returns them as regular strings.

            Parameters:
                byte_string(b_str): String in Byte format.

            Returns:
                str: String decoded to utf-8 or cp949.
                     If the execution environment is'Windows', it is converted to'cp949'.
                     If the execution environment is'Linux' or 'Mac OS', it is converted to'utf-8'.
        """

        _os = platform.system()
        if _os == 'Windows':
            return byte_string.decode('CP949')
        if _os == 'Linux' or _os == 'Darwin':
            return byte_string.decode('utf-8')

    @timer
    def run(self, command: str) -> NoReturn:
        """
        Execute the command.

            Parameters:
                command(str): Command to execute.
        """

        colored_print(f'Run: {command}', 'yellow')  # 커맨드 출력
        if command in get_command_black_list():  # 입력받은 커맨드가 실행하면 안되는 커맨드인지 체크
            colored_print('Out: Not supports', 'red')
            return  # 실행하면 안되는 커맨드라면 실행하지 않고 함수 종료
        popen = subprocess.Popen(args=shlex.split(command), shell=False, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)  # 커맨드를 실행함
        stdout, _ = popen.communicate()  # stderr 메세지는 무시한다
        colorname = 'green'
        result = self._convert_byte_to_string(stdout)
        if result.replace('\n', '').replace('\r', '') == '':  # 출력값이 아무것도 없는 경우에는 'None'으로 변경한다
            result = 'None'
            colorname = 'red'
        colored_print('Out:', colorname, end=' ')
        colored_print(f'{result}', 'white')  # 커맨드 실행결과 출력

    def run_all(self, command_list: List):
        """
        Executes all commands in the command list.

            Parameters:
                command_list(str): List of commands to be executed.
        """

        if equals(len(command_list), 0):
            colored_print('No command found.', 'orage')
        else:
            for command in command_list:
                self.run(command)


if __name__ == "__main__":
    c = CommandRunner()
    c.run_all(['python -V', 'pip -V', 'git --version', 'dir', 'pwd'])
