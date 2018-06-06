# coding = utf-8
# ae_h - 2018/6/5
from sklearn.model_selection import train_test_split, cross_val_score

from quant.models.base_model import BaseModel
from sklearn import linear_model, preprocessing
from sklearn import metrics
from quant.log.quant_logging import logger
from quant.models.k_data import MODULE_NAME
from quant.models.pca_model import PCAModel


class LinearRegressionModel(BaseModel):
    module_name = MODULE_NAME
    model_name = "linear_regression_model"

    def training_model(self, code, data, features, *args):

        X = data[features]
        # if not args:
        y = data['next_direction']

        # normalization
        X = preprocessing.scale(X)

        # pca缩放
        pca = PCAModel(self.module_name).load(code)
        X = pca.transform(X)

        X_train, x_test, y_train, y_test = train_test_split(X, y, test_size=.3, shuffle=False, random_state=10)

        LR_model = linear_model.LinearRegression(n_jobs=-1, normalize=True)

        LR_model.fit(X_train, y_train)

        y_pred = LR_model.predict(x_test)

        logger.debug('mse: %s' % metrics.mean_squared_error(y_test, y_pred))

        LR_model.fit(X, y)



    def predict(self, code, data):
        pass
