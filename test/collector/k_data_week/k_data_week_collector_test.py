import unittest

from collector.k_data_week.k_data_weekly_collector import collect_all, collect_all_weekly
import futuquant as ft

from common_tools.datetime_utils import get_current_date
from config import default_config
from dao.k_data import fill_market


class K_Data_Collector_Test(unittest.TestCase):
    def setUp(self):
        self.futu_quote_ctx = ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST,
                                                  port=default_config.FUTU_OPEND_PORT)

    def tearDown(self):
        self.futu_quote_ctx.close()

    def test_collect_all(self):
        collect_all(self.futu_quote_ctx)

    def test_collect_all_weekly(self):
        collect_all_weekly(self.futu_quote_ctx)

    def test_get_data(self):
        state, data = self.futu_quote_ctx.get_history_kline(fill_market('600196'), ktype='K_WEEK', autype='qfq',
                                                            start='2018-08-01',
                                                            end=get_current_date())

        print(data)
