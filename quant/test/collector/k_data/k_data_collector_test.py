import unittest

from quant.collector.k_data.k_data_collector import collect_all
from quant.test import before_run
import tushare as ts


class K_Data_Collector_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_collect_all(self):
        collect_all()

