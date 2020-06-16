from .file_reader import Reader


class ConfigReader(object):
    pass


if __name__ == "__main__":
    reader = Reader()
    conf = reader.read_yaml_file('data/foo.conf.yaml')
