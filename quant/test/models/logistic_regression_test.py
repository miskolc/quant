import unittest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from quant.test import before_run
from quant.models.logistic_regression_model import LogisticRegressionModel


class Logistic_Regression_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        model = LogisticRegressionModel()
        model.training_model("600196")
