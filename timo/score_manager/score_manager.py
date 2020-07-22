#-*- coding: utf-8 -*-

from collections import Counter
from decorators import timer
from file_manager.config_reader import ConfigReader
from test_manager.result_parser import Parser
from utils import color
from utils import colored_print



class ScoreCalculator(object):
    def __init__(self):
        self.conf = ConfigReader()
        self.parser = Parser()
        self.score_set = self._get_score_set()
        self.r = {
            'CSW': 0,
            'Unittest': 0,
            'Coverage': 0,
            'APItest': 0,
            'E2Etest': 0,
        }

    
    def _refine_test_name(self, test_name: str) -> str:
        if 'CSW' in test_name:
            test_name = 'CSW'
        elif 'Unittest' in test_name:
            test_name = 'Unittest'
        elif 'Coverage' in test_name:
            test_name = 'Coverage'
        elif 'APITest' in test_name:
            test_name = 'APITest'
        elif 'E2Etest' in test_name:
            test_name = 'E2Etest'
        return test_name

    def _get_score_set(self) -> dict:
        r = {
            'CSW': 0,
            'Unittest': 0,
            'Coverage': 0,
            'APItest': 0,
            'E2Etest': 0,
        }
        score_set = self.conf.get_score_info()
        for key, value in score_set.items():
            key = self._refine_test_name(key)
            r[key] = float(value.rstrip('%')) * 0.01
        return r
            



    def _get_test_results(self) -> list:

        r = []
        tests = self.conf.get_tests()
        for test in tests:
            info = self.conf.get_report_info(test)
            r.append(
                {
                    'name': self._refine_test_name(test),
                    'result': self.parser.parse(
                        kind=test,
                        file_type=info['type'],
                        test_tool=self.conf.get_test_tool(test)['uses']
                    )
                }
            )
        return r

    @timer
    def calculate(self) -> dict:
        score = {
            'CSW': {'score': 0, 'count': 0},
            'Unittest': {'score': 0, 'count': 0},
            'Coverage': {'score': 0, 'count': 0},
            'APItest': {'score': 0, 'count': 0},
            'E2Etest': {'score': 0, 'count': 0},
        }
        r = self._get_test_results()
        def csw(data: dict) -> float:
            score = (1 - (data['warning'] / 100))
            score = -1 if score < -1 else score
            score *= self.score_set['CSW']
            return score

        def unittest(data: dict) -> float:
            total = sum(data.values())
            success_rate = data['success'] / total
            score = success_rate * self.score_set['Unittest']
            return score

        def coverage(data: dict) -> float:
            return (data['test_val'] / 100) * self.score_set['Coverage']

        def apitest(data: dict) -> float:
            total = sum(data.values())
            success_rate = data['success'] / total
            score = success_rate * self.score_set['APITest']
            return score

        def e2etest(data: dict) -> float:
            total = sum(data.values())
            success_rate = data['success'] / total
            score = success_rate * self.score_set['E2Etest']
            return score


        for data in r:
            if data['name'] == 'CSW':
                score['CSW']['score'] += csw(data['result'])
                score['CSW']['count'] += 1
            elif data['name'] == 'Unittest':
                score['Unittest']['score'] += unittest(data['result'])
                score['Unittest']['count'] += 1
            elif data['name'] == 'Coverage':
                score['Coverage']['score'] += coverage(data['result'])
                score['Coverage']['count'] += 1
            elif data['name'] == 'APITest':
                score['APITest']['score'] += apitest(data['result'])
                score['APITest']['count'] += 1
            elif data['name'] == 'E2Etest':
                score['E2Etest']['score'] += e2etest(data['result'])
                score['E2Etest']['count'] += 1

        res = sum([(data['score'] / data['count']) for data in score.values() if data['count'] != 0]) * 10

        print()
        colored_print('🚀 {:<17}'.format('Test results'), colorname='white')
        colored_print('-' * 19, colorname='white')
        for test, value in score.items():
            _score = value['score'] / value['count'] if value['count'] != 0 else 0
            fstr = f'{_score * 10:>6.2f}' if _score != 0 else '{:>5}'.format('❌')
            colored_print(f'{test:<10}', colorname='white', end='')
            colored_print(' → ', colorname='cyan', end='')
            colored_print(f'{fstr}', colorname='green')
        colored_print('-' * 19, colorname='white')
        colored_print('{:<10}'.format('Total'), colorname='white', end='')
        colored_print(' → ', colorname='cyan', end='')
        colored_print(f'{res:>6.2f}', colorname='blue')
        print()

        return res



if __name__ == "__main__":
    s = ScoreCalculator()
    s.calculate()