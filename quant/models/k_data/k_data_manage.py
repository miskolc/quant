import tushare as ts
from quant.dao.k_data_dao import k_data_dao
from quant.models.k_data.logistic_regression_classifier import LogisticRegressionClassifier
from quant.models.k_data.pca_model import PCAModel
from quant.models.k_data.support_vector_classifier import SupportVectorClassifier
from quant.models.k_data.random_forest_classifier import RandomForestClassifierModel
from quant.models.k_data.xgboost_classifier import XGBoostClassier
from quant.models.k_data.sequantial_neural import SequantialNeural
from datetime import datetime
from quant.dao.index_k_data_dao import index_k_data_dao
from quant.dao.k_data_predict_log_dao import k_data_predict_log_dao
from quant.log.quant_logging import logger


# 训练K_data模型
def training_k_data():
    df = ts.get_hs300s()
    for code in df['code'].values:
        try:
            logger.debug('begin training mode, code:%s' % code)
            data, features = k_data_dao.get_k_data_with_features(code, '2015-01-01',
                                                                 datetime.now().strftime("%Y-%m-%d"))

            pac = PCAModel()
            lr = LogisticRegressionClassifier()
            svc = SupportVectorClassifier()
            rf = RandomForestClassifierModel()
            xgb = XGBoostClassier()
            ann = SequantialNeural()

            pac.training_model(code, data, features)
            lr.training_model(code, data, features)
            svc.training_model(code, data, features)
            rf.training_model(code, data, features)
            xgb.training_model(code, data, features)
            ann.training_model(code, data, features)
            logger.debug('training mode end, code:%s' % code)
        except Exception as e:
            logger.error(e)

# 预测K_data
def predict_k_data():
    df = ts.get_hs300s()
    df_index = index_k_data_dao.get_rel_price();

    for code in df['code'].values:
        try:

            logger.debug('begin predict, code:%s' % code)
            data, features = k_data_dao.get_k_predict_data_with_features(code, df_index)

            lr = LogisticRegressionClassifier()
            svc = SupportVectorClassifier()
            rf = RandomForestClassifierModel()
            xgb = XGBoostClassier()
            ann = SequantialNeural()

            lr_pred = lr.predict(code, data)
            svc_pred = svc.predict(code, data)
            rf_pred = rf.predict(code, data)
            xgb_pred = xgb.predict(code, data)
            ann_pred = ann.predict(code, data)

            k_data_predict_log_dao.insert(code, logistic_regression=lr_pred,
                                          support_vector_classifier=svc_pred,
                                          random_forest_classifier=rf_pred,
                                          xgb_classifier=xgb_pred,
                                          sequantial_neural=ann_pred
                                          )
            logger.debug('predict end, code:%s' % code)
        except Exception as e:
            logger.error(e)


"""
    1. 训练k_data模型
    2. 预测k_data
"""
def launch():
    training_k_data()
    predict_k_data()
