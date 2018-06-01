# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/28
from sklearn.decomposition import PCA
from sklearn.externals import joblib
from quant.models.base_model import BaseModel
from quant.common_tools.decorators import exc_time

class PCAModel(BaseModel):
    model_name = 'pac'

    @exc_time
    def training_model(self, code, data, features):
        pca = PCA(n_components=None)
        pca.fit(data[features])
        # 输出模型
        joblib.dump(pca, self.get_model_path(code, self.model_name))

    def load(self, code):
        pca = joblib.load(self.get_model_path(code, self.model_name))
        return pca