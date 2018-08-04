import unittest

from dao.basic.stock_dao import stock_dao


class StrategyTest(unittest.TestCase):

    def test_query_by_code(self):
        stock = stock_dao.query_by_code('600196')

        print(stock)