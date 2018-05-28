import unittest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from quant.test import before_run
from quant.models.support_vector_classifier import SupportVectorClassifier


class Support_Vector_Classifier_test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        model = SupportVectorClassifier()
        model.training_model("600196")
