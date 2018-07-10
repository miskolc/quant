import unittest
from quant.test import before_run
from quant.dao.basic.trade_date_dao import trade_date_dao


class Trade_Date_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_init_pool(self):
        trade_date_dao.init_pool();

    def test_is_holiday(self):
        rs = trade_date_dao.is_holiday('2018-07-08')
        print(rs)