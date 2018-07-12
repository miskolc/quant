# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from common_tools import exc_time
from sqlalchemy import MetaData, select, and_
from dao.data_source import dataSource
from sqlalchemy import Table
from common_tools import datetime_utils
from sqlalchemy.sql import text
from log.quant_logging import logger
import pandas as pd

class K_Data_Predict_Log_Dao:
    @exc_time
    def insert(self, code, logistic_regression, random_forest_classifier, support_vector_classifier, xgb_classifier,
               sequantial_neural):
        sql = text('replace into k_data_predict_log (date, code, '
                   'logistic_regression, '
                   'random_forest_classifier, '
                   'support_vector_classifier, '
                   'xgb_classifier, '
                   'sequantial_neural) '
                   'values(:date,:code,:logistic_regression,:random_forest_classifier,:support_vector_classifier,:xgb_classifier,:sequantial_neural)')

        result = dataSource.mysql_quant_conn.execute(sql, date=datetime_utils.get_current_date(),
                                                     code=code,
                                                     logistic_regression=logistic_regression,
                                                     random_forest_classifier=random_forest_classifier,
                                                     support_vector_classifier=support_vector_classifier,
                                                     xgb_classifier=xgb_classifier,
                                                     sequantial_neural=sequantial_neural)

        return result

    # 获取每日的predict report
    @exc_time
    def get_predict_log_list(self, date):
        sql = text('''
                SELECT
                  s.bk_name,
                  s.name,
                  k.code,
                  k.date,
                  (k.support_vector_classifier + k.logistic_regression + k.xgb_classifier + k.sequantial_neural +
                   k.random_forest_classifier) vote_score,
                
                  (SELECT max(test_score)
                   FROM k_data_model_log kdml
                   WHERE kdml.code = k.code AND kdml.date = date_format(current_date - INTERVAL 1 DAY, '%Y-%m-%d')
                   GROUP BY kdml.code) AS      max_test_score
                
                
                FROM k_data_predict_log k
                  INNER JOIN stock_industry s ON k.code = s.code
                
                WHERE
                  (k.support_vector_classifier + k.logistic_regression + k.xgb_classifier + k.sequantial_neural +
                   k.random_forest_classifier) >= 2
                  AND k.date = :date
                ORDER BY s.bk_code, s.code
        ''' )

        df = pd.read_sql(sql=sql, params={ "date": date,}
                         , con=dataSource.mysql_quant_conn)

        return df


k_data_predict_log_dao = K_Data_Predict_Log_Dao()
