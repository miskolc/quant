import unittest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split

from quant.dao.data_source import dataSource
from quant.test import before_run
from quant.models.support_vector_classifier import SupportVectorClassifier
import pandas as pd

def f(x):
    if x > 0:
        return 1
    elif x is None:
        return None
    else:
        return 0


class Support_Vector_Classifier_test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        model = SupportVectorClassifier()
        model.training_model("600196")
