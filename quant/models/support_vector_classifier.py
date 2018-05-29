# ae_h - 2018/5/28

from datetime import datetime
from sklearn import preprocessing
from sklearn import svm
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV
from quant.dao.k_data_dao import k_data_dao
from quant.feature_utils.feature_collector import collect_features
from quant.log.quant_logging import quant_logging as logging
from quant.models.base_model import BaseModel


class SupportVectorClassifier(BaseModel):
    def training_model(self, code):
        data = k_data_dao.get_k_data(code, '2015-01-01', datetime.now().strftime("%Y-%m-%d"))

        data, features = collect_features(data)

        X_train, X_test, y_train, y_test = train_test_split(data[features], data['next_direction'], test_size=.3,
                                                            shuffle=False)

        tuned_parameters = [
            {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}
        ]

        # normalization
        X_train = preprocessing.scale(X_train)
        X_test = preprocessing.scale(X_test)

        # pca缩放
        pca = PCA(n_components=None)
        pca.fit(X_train)
        X_train = pca.transform(X_train)


        # # tsne缩放
        # X_train = TSNE(n_components=2, learning_rate=100).fit_transform(X_train)
        # X_test = TSNE(n_components=2, learning_rate=100).fit_transform(X_test)

        # 网格搜寻最优参数
        grid = GridSearchCV(svm.SVC(), tuned_parameters)
        grid.fit(X_train, y_train)

        logging.logger.debug(grid.best_estimator_)  # 训练的结果
        logging.logger.debug("Support Vector Classifier's best score: %.2f" % grid.best_score_)  # 训练的评分结果

        support_vector_classifier = grid.best_estimator_
        # 使用训练数据, 重新训练
        support_vector_classifier.fit(X_train, y_train)

        # 使用测试数据对模型进评平分
        y_test_pred = support_vector_classifier.predict(X_test)

        # 在测试集中的评分
        logging.logger.debug('accuracy score: %.2f' % accuracy_score(y_test, y_test_pred))

        # 使用所有数据, 重新训练
        support_vector_classifier.fit(data[features], data['next_direction'])
