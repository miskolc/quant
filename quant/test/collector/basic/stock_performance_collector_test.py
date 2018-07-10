import unittest

from quant.collector.basic.stock_basic_collector import  collect_stock_basic
from quant.test import before_run
import tushare as ts

class Stock_Basic__Test(unittest.TestCase):
    def setUp(self):
        before_run()


    def test_collect_stock_basic(self):
        collect_stock_basic()