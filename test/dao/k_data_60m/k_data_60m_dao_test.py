import unittest

from dao.k_data_60m.k_data_60m_dao import k_data_60m_dao


from log.quant_logging import logger
from test import before_run


class K_Data_60m_Dao_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_get_k_data(self):
        df = k_data_60m_dao.get_k_data("600196", start='2018-05-01', end='2018-06-04')
        logger.debug(df.head())



