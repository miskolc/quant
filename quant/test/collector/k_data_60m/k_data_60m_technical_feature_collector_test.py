import unittest
from quant.test import before_run
import quant.collector.k_data_60m.k_data_60m_technical_feature_collector as kdtfc
import tushare as ts
from quant.log.quant_logging import logger


class K_Data_60m_Technical_Collector_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def collect_single_test(self):
        df = ts.get_hs300s()

        for code in df['code'].values:
            try:
                kdtfc.collect_single(code, start='2018-05-04', end='2018-06-05')
            except Exception as e:
                logger.error("collect technical features failed code:%s, exception:%s" % (code, repr(e)))
