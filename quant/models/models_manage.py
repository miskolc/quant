# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

import os
import sys

# Append project path to system path
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

from quant.log.quant_logging import quant_logging as logging
from quant.config import default_config
from sqlalchemy import create_engine, MetaData
from quant.dao.data_source import dataSource
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

PROJECT_NAME = "quant-collector"


def init_db():
    # 如果配置DATABASE_QUANT_URI属性, 实例化mysql_quant_engine
    if default_config.DATABASE_QUANT_URI:
        # 使用单例模式保存数据库engine
        mysql_quant_engine = create_engine(default_config.DATABASE_QUANT_URI, encoding='utf8',
                                           convert_unicode=True, pool_size=100, pool_recycle=1200)
        dataSource.mysql_quant_engine = mysql_quant_engine
        dataSource.mysql_quant_conn = mysql_quant_engine.connect()
        dataSource.mysql_quant_metadata = MetaData(dataSource.mysql_quant_conn)


def init_logger():
    # 使用单例模式保存logger
    logging.create_logger(default_config.DEBUG, PROJECT_NAME)


# 训练K_data模型
def training_k_data():
    df = ts.get_hs300s()
    for code in df['code'].values:
        logging.logger.debug('begin training mode, code:%s' % code)
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

# 预测K_data
def predict_k_data():
    df = ts.get_hs300s()
    df_index = index_k_data_dao.get_rel_price();

    for code in df['code'].values:
        logging.logger.debug('begin predict, code:%s' % code)
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


if __name__ == '__main__':
    init_logger()
    init_db()

    training_k_data()
    predict_k_data()
    # schedule.every().day.at("15:30").do(k_data.collect_hs300_daily)

    '''
    while True:
        schedule.run_pending()
        time.sleep(1)
    '''
