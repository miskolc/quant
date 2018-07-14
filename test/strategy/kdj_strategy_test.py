# ae_h - 2018/7/14
import unittest
from pitcher.kdj_st import KDJStrategy
from pitcher.context import Context

class KDJStrategyTest(unittest.TestCase):

    def test_handle_data(self):
        kdj = KDJStrategy()
        kdj.handle_data(context=Context())

