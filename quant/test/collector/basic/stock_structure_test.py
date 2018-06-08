import unittest
from quant.test import before_run
from quant.collector.basic import stock_structure_collector


class Stock_Industry_Classified_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_collect_industry(self):
        stock_structure_collector.collect_all();
