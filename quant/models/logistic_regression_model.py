# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/28

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from quant.dao.k_data_dao import k_data_dao
from datetime import datetime
from quant.log.quant_logging import quant_logging as logging
from quant.models.base_model import BaseModel

features = ['close', 'low', 'high', 'volume', 'open']


class LogisticRegressionModel(BaseModel):

    """
        1. 70% training/grid search 选择超参数
        2. 30% test
    """
    def training_model(self, code):
        # 从数据库中获取2015-01-01到今天的所有数据
        data = k_data_dao.get_k_data(code, '2015-01-01', datetime.now().strftime("%Y-%m-%d"))

        # 数据按30%测试数据, 70%训练数据进行拆分
        X_train, X_test, y_train, y_test = train_test_split(data[features], data['next_direction'], test_size=.3,
                                                            shuffle=False)

        # 交叉验证查找合适的超参数: penalty, C
        # penalty
        tuned_parameters = {
            'penalty': ['l1', 'l2'],
            'C': [0.001, 0.01, 0.1, 1, 10, 100]
        }

        grid = GridSearchCV(LogisticRegression(), tuned_parameters, cv=None, n_jobs=-1)
        grid.fit(X_train, y_train)  # 网格搜索训练
        logging.logger.debug(grid.best_estimator_)  # 训练的结果
        logging.logger.debug("logistic regression's best score: %.2f" % grid.best_score_)  # 训练的结果

        logistic_regression = grid.best_estimator_
        # 使用训练数据, 重新训练
        logistic_regression.fit(X_train, y_train)

        # 使用测试数据对模型进行平分
        test_score = logistic_regression.score(X_test, y_test)

        # 在测试集中的评分
        logging.logger.debug("Test score: %.2f" % test_score)

        # 使用所有数据, 重新训练
        logistic_regression.fit(data[features], data['next_direction'])





