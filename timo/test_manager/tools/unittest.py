from file_manager.file_reader import Reader
import glob


class UnittestParser(object):
    def __init__(self):
        self.reader = Reader()

    def parse(self, path: str, file_type: str) -> dict:
        return_val = {
            'success': 0,
            'fail': 0,
            'skip': 0
        }
        if file_type == 'xml':
            xml = self.reader.read_xml_file(path)
            data = xml['testsuites']['testsuite']
            total = int(data['@tests'])
            fail = int(data['@failures']) + int(data['@errors'])
            skip = int(data['@skipped'])
            success = total - fail - skip
            return_val['success'] = success
            return_val['fail'] = fail
            return_val['skip'] = skip
        elif file_type == 'html':
            report_list = glob.glob(path + '/*.html')
            for file in report_list:
                html = self.reader.read_html_file(file)
                data = html['html']['body']['div']['div'][0]['div']['p'][2]['text']
                data = [x.rstrip(',').rstrip(':') for x in data.split()]
                r = {}
                for i in range(0, len(data), 2):
                    r[data[i]] = data[i + 1]
                return_val['success'] += int(r['Pass']) if 'Pass' in r else 0
                return_val['fail'] += int(r['Fail']) if 'Fail' in r else 0
                return_val['skip'] += int(r['Skip']) if 'Skip' in r else 0

        return return_val
