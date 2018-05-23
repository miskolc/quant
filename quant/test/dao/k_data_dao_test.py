import unittest
from quant.test import before_run
from quant.dao.k_data_dao import k_data_dao
from quant.log.quant_logging import quant_logging as logging


class K_Data_Dao_Test(unittest.TestCase):

    def setUp(self):
        before_run()

    def get_k_data_test(self):

        df = k_data_dao.get_k_data("600000", start="2015-01-01", end="2018-05-21")
        logging.logger.debug(df.head())
        self.assertIsNotNone(df)




