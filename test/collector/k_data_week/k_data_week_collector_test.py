import unittest

from collector.k_data_week.k_data_week_collector import collect_all,collect_all_weekly
import futuquant as ft

from config import default_config


class K_Data_Collector_Test(unittest.TestCase):

    def setUp(self):
        self.futu_quote_ctx = ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST, port=default_config.FUTU_OPEND_PORT)

    def tearDown(self):
        self.futu_quote_ctx.close()

    def test_collect_all(self):
        collect_all(self.futu_quote_ctx)

    def test_collect_all_weekly(self):
        collect_all_weekly(self.futu_quote_ctx)
