from unittest import TestCase
from app.urls import URLFinder


class TestURLFinder(TestCase):
    def test_choose_url(self):
        test_json_response = {'webPages': {'value': [{'url': 'bloomberg'},
                                                     {'url': 'testwebsite'}]}}
        result = URLFinder().choose_url(results_json=test_json_response)
        self.assertEqual('testwebsite', result)

