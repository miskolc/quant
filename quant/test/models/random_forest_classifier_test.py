# coding = utf-8
# ae_h - 2018/5/30

import unittest
from quant.models.random_forest_classifier import RandomForestClassifierModel
from quant.test import before_run


class Random_Forest_Classifier_test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        model = RandomForestClassifierModel()
        model.training_model("600196")
