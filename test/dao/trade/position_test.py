# ae_h - 2018/7/27

import unittest

from config import default_config
from dao.trade.position_dao import Position_Dao
import futuquant as ft

class PositionTest(unittest.TestCase):

    def setUp(self):
        self.futu_quote_ctx = ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST,
                                                  port=default_config.FUTU_OPEND_PORT)

    def tearDown(self):
        self.futu_quote_ctx.close()

    def test_query(self):
        position_dao = Position_Dao()
        position_dao.query_by_code('601800')