# coding =utf-8
# ae_h - 2018/6/4
import unittest

from quant.test import before_run
from quant.strategy import pair_selection


class PairStrategyTest(unittest.TestCase):

    def setUp(self):
        before_run()

    def test_strategy(self):

        pai