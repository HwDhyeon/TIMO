from decorators import timer
from file_manager.config_reader import ConfigReader
from utils import colored_print
from utils import get_command_black_list
from typing import List
from typing import NoReturn
import subprocess
import shlex


class TestRunner(object):
    """Perform tests."""
    
    @timer
    def run(self, command: str) -> NoReturn:
        """
        Execute the command.

            Parameters:
                command(str): Command to execute.
        """

        colored_print(f'Run: {command}', 'yellow') # 커맨드 출력
        if command in get_command_black_list(): # 입력받은 커맨드가 실행하면 안되는 커맨드인지 체크
            colored_print(f'Out: Not supports', 'red')
            return # 실행하면 안되는 커맨드라면 실행하지 않고 함수 종료
        popen = subprocess.Popen(args=command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE) # 커맨드를 실행함
        stdout, _ = popen.communicate() # stderr 메세지는 무시한다
        colorname = 'green'
        if (result := stdout.decode('utf-8').replace('\n', '').replace('\r', '')) == '': # 출력값이 아무것도 없는 경우에는 'None'으로 변경한다
            result = 'None'
            colorname = 'red'
        colored_print(f'Out: {result}', colorname) # 커맨드 실행결과 출력

    def run_all(self, command_list: List):
        """
        Executes all commands in the command list.

            Parameters:
                command_list(str): List of commands to be executed.
        """

        for command in command_list:
            self.run(command)


if __name__ == "__main__":
    c = TestRunner()
    c.run_all(['python -V', 'pip -V', 'git --version', 'dir', 'pwd'])
