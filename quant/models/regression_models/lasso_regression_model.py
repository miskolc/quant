# coding = utf-8
# ae_h - 2018/6/5
from sklearn.model_selection import train_test_split, cross_val_score

from quant.models.base_model import BaseModel
from sklearn import linear_model, preprocessing
from sklearn.metrics import accuracy_score
from quant.log.quant_logging import logger
from quant.models.k_data import MODULE_NAME
from quant.models.pca_model import PCAModel


class LassoRegressionModel(BaseModel):
    module_name = MODULE_NAME
    model_name = "linear_regression_model"

    def training_model(self, code, data, features, *args):
        X = data[features]
        y = data[args]

        # normalization
        X = preprocessing.scale(X)

        # pca缩放
        pca = PCAModel(self.module_name).load(code)
        X = pca.transform(X)

        X_train, x_test, y_train, y_test = train_test_split(X, y, test_size=.3, shuffle=False)

        lasson_model = linear_model.LassoCV(n_jobs=-1, random_state=10)

        lasson_model.fit(X_train, y_train)

        y_pred = cross_val_score(lasson_model, x_test)

        test_score = accuracy_score(y_test, y_pred)

        logger.debug('test score %s ' %test_score)

        lasson_model.fit(X, y)

        full_set_score = lasson_model.score(X, y)

        logger.debug('full set score %s' % full_set_score)

    def predict(self, code, data):
        pass
