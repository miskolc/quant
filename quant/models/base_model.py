# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/28

import abc
from quant.config import default_config
import os


class BaseModel:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def training_model(self, code, data, features):
        """training model"""
        return

    @abc.abstractmethod
    def predict(self, code, data):
        """training model"""
        return

    # 输出路径类似: /k_data/logistic_regression_classifier/logistic_regression_classifier_60000.pkl
    def get_model_path(self, code, module_name, model_name, suffix='pkl'):
        dir = os.path.join(os.path.join(default_config.MODELS_OUTPUT_DIR, module_name), model_name)
        if not os.path.exists(dir):
            os.makedirs(dir)

        return '%s/%s_%s.%s' % (dir, model_name, code, suffix)
