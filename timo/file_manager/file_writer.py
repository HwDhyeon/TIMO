from timo.utils import equals
from typing import Any
import json
import yaml
import csv


class Writer(object):

    def write_file(self, path: str, content: Any, ext: str) -> bool:

        def _save(data: Any, *, ext=''):
            with open(file=path, mode='w', encoding='utf-8') as f:
                if equals(ext, 'csv'):
                    wr = csv.writer(f)
                    wr.writerows(data)
                else:
                    f.write(data)

        try:
            if equals(ext, 'json'):
                _save(json.dumps(content, indent='    '))
            elif equals(ext, 'yaml') or equals(ext, 'yml'):
                _save(yaml.dump(content, indent=4))
            else:
                _save(content, ext='csv')
        except Exception as e:
            print(e)
            return False
        else:
            return True
