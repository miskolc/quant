import unittest

from dao.k_data_weekly.k_data_weekly_dao import k_data_week_dao
from test import before_run


class K_Data_Week_Dao_Test(unittest.TestCase):

    def setUp(self):
        before_run()

    def test_get_k_data(self):
        df = k_data_week_dao.get_k_data('SH.600196', '2018-05-01','2018-07-06')

        print(df)


