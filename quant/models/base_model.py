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

    def get_model_path(self, code, model_name):

        dir = os.path.join(default_config.MODELS_OUTPUT_DIR,model_name)
        if not os.path.exists(dir):
            os.makedirs(dir)

        return '%s/%s_%s.pkl' % (dir, model_name,code)


