from timo.file_handler import fileIO
import os


class Config(object):
    def __init__(self):
        self.io = fileIO.File_IO_Tool()
        self.config = self._read_config_file()

    def _read_config_file(self) -> dict:
        path = os.path.dirname(os.path.abspath(__file__)) + '\\' + 'config.path.txt'
        if not os.path.isfile(path):
            raise FileNotFoundError
        path = self.io.read_file(path)
        return self.io.read_file(path)


cf = Config()
print(cf.config)
