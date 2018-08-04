# ae_h - 2018/7/27

import unittest

from config import default_config
from dao.trade.position_dao import Position_Dao
import futuquant as ft

from dao.trade.target_dao import target_dao


class TargetTest(unittest.TestCase):

    def setUp(self):
        self.futu_quote_ctx = ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST,
                                                  port=default_config.FUTU_OPEND_PORT)

    def tearDown(self):
        self.futu_quote_ctx.close()

    def test_query(self):
        target = target_dao.query_by_code(strategy_code='custom', code='600196')
        print(target.name)