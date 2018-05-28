# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/28

import abc


class BaseModel:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def training_model(self, code):
        """training model"""
        return


