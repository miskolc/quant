import unittest
from dao.trade.strategy_dao import strategy_dao

class StrategyTest(unittest.TestCase):

    def test_query_all(self):
        strategries = strategy_dao.query_all()

        print(strategries)