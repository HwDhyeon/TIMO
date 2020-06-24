from typing import Any
import json
import yaml
import csv


class Writer(object):
    def write_file(self, path: str, content: Any, ext: str) -> bool:
        pass