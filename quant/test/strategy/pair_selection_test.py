# coding =utf-8
# ae_h - 2018/6/4
import os
import sys

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

import unittest

from quant.test import before_run
from quant.strategy.pair.pair_selection import code_muning, cal_pair_stocks, cal_p_value
import tushare as ts


class PairStrategyTest(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_strategy(self):
        data = ts.get_sz50s()
        code_set = code_muning(data)
        cal_pair_stocks(code_set)

    def test_cal_p_value(self):
        pair_set = set()
        pair_set.add(('600519', '000858'))
        cal_pair_stocks(pair_set)