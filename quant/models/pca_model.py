# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/28
from sklearn.decomposition import PCA
from sklearn.externals import joblib
from quant.models.base_model import BaseModel
from quant.common_tools.decorators import exc_time
from sklearn import preprocessing

class PCAModel(BaseModel):
    model_name = 'pca'

    @exc_time
    def training_model(self, code, data, features):
        X = data[features]
        X = preprocessing.scale(X)

        pca = PCA(n_components=None)
        pca.fit(X)
        # 输出模型
        joblib.dump(pca, self.get_model_path(code, self.model_name))

    def load(self, code):
        pca = joblib.load(self.get_model_path(code, self.model_name))
        return pca
