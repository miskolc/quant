import unittest

from dao.trade.position_dao import position_dao


class Position_Dao_Test(unittest.TestCase):
    def test_get_list(self):
        list = position_dao.get_position_list()

        for position in list:
            print(position.code, position.price, position.total_market)
