"""Unit-тесты клиента"""

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
import client

test_presense = client.Client.status_presence()
test_asnwer = client.Client.process_answer


class TestClass(unittest.TestCase):
    """
    Класс с тестами
    """

    def test_def_presense(self):
        """Тест коректного запроса"""
        test_presense[TIME] = 1.1  # время необходимо приравнять принудительно иначе тест никогда не будет пройден
        self.assertEqual(test_presense, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_200_ans(self):
        """Тест корректтного разбора ответа 200"""
        self.assertEqual(test_asnwer({RESPONSE: 200}), '200 : OK')

    def test_400_ans(self):
        """Тест корректного разбора 400"""
        self.assertEqual(test_asnwer({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_no_response(self):
        """Тест исключения без поля RESPONSE"""
        self.assertRaises(ValueError, test_asnwer, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
