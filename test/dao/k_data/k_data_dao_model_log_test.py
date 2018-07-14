import unittest

from dao.k_data.k_data_model_log_dao import k_data_model_log_dao as k_data_model_log_dao
from test import before_run


class K_Data_Dao_Model_Log_Test(unittest.TestCase):

    def setUp(self):
        before_run()

    def test_insert(self):
        k_data_model_log_dao.insert(code='600179', name='logistic_regression'
                                , best_estimator='logistic_regression_model', train_score=0.55, test_score=0.66)


    def test_exists(self):
        k_data_model_log_dao.exists('600196')



