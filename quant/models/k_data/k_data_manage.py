from datetime import datetime

import tushare as ts
from quant.dao.k_data.k_data_dao import k_data_dao
from quant.dao.k_data.k_data_predict_log_dao import k_data_predict_log_dao

from quant.dao.k_data.index_k_data_dao import index_k_data_dao
from quant.log.quant_logging import logger
from quant.models.k_data.logistic_regression_classifier import LogisticRegressionClassifier
from quant.models.k_data.random_forest_classifier import RandomForestClassifierModel
#from quant.models.k_data.sequantial_neural_classifier import SequantialNeuralClassifier
from quant.models.k_data.support_vector_classifier import SupportVectorClassifier
from quant.models.k_data.xgboost_classifier import XGBoostClassier
from quant.models.pca_model import PCAModel
from quant.dao.basic.stock_pool_dao import stock_pool_dao


# 训练K_data模型
def training_k_data(start, end):
    df = stock_pool_dao.get_list()
    codes = df['code'].values[start: end]
    for code in codes:
        try:
            logger.debug('begin training mode, code:%s' % code)
            data, features = k_data_dao.get_k_data_with_features(code, '2015-01-01',
                                                                 datetime.now().strftime("%Y-%m-%d"))

            pca = PCAModel('k_data')
            lr = LogisticRegressionClassifier()
            svc = SupportVectorClassifier()
            rf = RandomForestClassifierModel()
            xgb = XGBoostClassier()
            #ann = SequantialNeuralClassifier()

            pca.training_model(code, data, features)
            lr.training_model(code, data, features)
            svc.training_model(code, data, features)
            rf.training_model(code, data, features)
            xgb.training_model(code, data, features)
            #ann.training_model(code, data, features)

            logger.debug('training mode end, code:%s' % code)
        except Exception as e:
            logger.error("training k data error, code:%s, error:%s" % (code, repr(e)))


# 预测K_data
def predict_k_data():
    df = stock_pool_dao.get_list()
    df_index = index_k_data_dao.get_rel_price();

    for code in df['code'].values:
        try:

            logger.debug('begin predict, code:%s' % code)
            data, features = k_data_dao.get_k_predict_data_with_features(code, df_index)

            lr = LogisticRegressionClassifier()
            svc = SupportVectorClassifier()
            rf = RandomForestClassifierModel()
            xgb = XGBoostClassier()
            #ann = SequantialNeuralClassifier()

            lr_pred = lr.predict(code, data[features])
            svc_pred = svc.predict(code, data[features])
            rf_pred = rf.predict(code, data[features])
            xgb_pred = xgb.predict(code, data[features])
            #ann_pred = ann.predict(code, data[features])

            k_data_predict_log_dao.insert(code, logistic_regression=lr_pred,
                                          support_vector_classifier=svc_pred,
                                          random_forest_classifier=rf_pred,
                                          xgb_classifier=xgb_pred,
                                          sequantial_neural=0
                                          )
            logger.debug('predict end, code:%s' % code)


        except Exception as e:
            logger.error("predict k data error, code:%s, error:%s" % (code, repr(e)))
