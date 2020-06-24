from file_manager.config_reader import ConfigReader
import subprocess
import shlex

class TestRunner(object):
    """테스트를 수행합니다."""

    def __init__(self):
        self.conf = ConfigReader()
    
    def run(self, command: str):
        popen = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = popen.communicate()
        print(stdout)
