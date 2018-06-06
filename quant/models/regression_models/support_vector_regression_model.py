# ae_h - 2018/6/6
import os
from sklearn import svm, preprocessing, metrics, logger
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split, GridSearchCV

from quant.common_tools.decorators import exc_time
from quant.dao.k_data.k_data_model_log_dao import k_data_model_log_dao
from quant.models.base_model import BaseModel
from quant.models.k_data import MODULE_NAME
from quant.models.pca_model import PCAModel


class SupportVectorRegressionModel(BaseModel):
    module_name = MODULE_NAME
    model_name = "support_vector_regression_model"

    def training_model(self, code, data, features, *args):
        X = data[features]
        y = data['close']

        # normalization
        X = preprocessing.scale(X)

        # pca缩放
        pca = PCAModel(self.module_name).load(code)
        X = pca.transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, shuffle=False, random_state=10)

        tuned_parameters = [
            {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}
        ]

        svr_model = GridSearchCV(svm.SVR(), tuned_parameters, n_jobs=-1)

        svr_model.fit(X_train, y_train)

        test_score = svr_model.score(X_test, y_test)

        y_pred = svr_model.predict(X_test)

        mse = metrics.mean_squared_error(y_test, y_pred)

        mse = '%.4e' % mse

        # full data set training

        svr_model.fit(X, y)

        # 记录日志
        k_data_model_log_dao.insert(code=code, name=self.model_name
                                    , best_estimator=svr_model,
                                    train_score=test_score, test_score=mse)

        # 输出模型
        joblib.dump(svr_model, self.get_model_path(code, self.module_name, self.model_name))

    @exc_time
    def predict(self, code, data):
        model_path = self.get_model_path(code, self.module_name, self.model_name)

        if not os.path.exists(model_path):
            logger.error('model not found, code is %s:' % code)
            return

        X = preprocessing.scale(data)
        pac = PCAModel(self.module_name).load(code)
        X = pac.transform(X)

        support_vector_regression_model = joblib.load(model_path)

        y_pred = support_vector_regression_model.predict(X)

        return int(y_pred[0])
