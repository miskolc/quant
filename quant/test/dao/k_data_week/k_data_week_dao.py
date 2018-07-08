import unittest

from quant.dao.k_data_week.k_data_week_dao import k_data_week_dao
from quant.test import before_run


class K_Data_Week_Dao_Test(unittest.TestCase):

    def setUp(self):
        before_run()

    def test_get_k_data(self):
        df = k_data_week_dao.get_k_data('600196', '2018-05-01','2018-07-06')

        print(df)



