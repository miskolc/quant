import unittest
from quant.test import before_run
from quant.dao.index_k_data_dao import index_k_data_dao
from quant.log.quant_logging import logger


class Index_K_Data_Dao_Test(unittest.TestCase):

    def setUp(self):
        before_run()

    def get_index_k_data_test(self):

        df = index_k_data_dao.get_k_data("^HSI", start="2018-01-01", end="2018-05-21")
        logger.debug(df.head())
        self.assertIsNotNone(df)

    def get_sh_k_data(self):
        df = index_k_data_dao.get_sh_k_data( start="2018-01-01", end="2018-05-21")
        logger.debug(df.head())
        self.assertIsNotNone(df)



