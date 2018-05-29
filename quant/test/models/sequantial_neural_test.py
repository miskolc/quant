# coding = utf-8
# ae_h - 2018/5/29

import unittest
from quant.models.sequantial_neural import SequantialNeural
from quant.test import before_run


class Support_Vector_Classifier_test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_training(self):
        model = SequantialNeural()
        model.training_model("600196")
