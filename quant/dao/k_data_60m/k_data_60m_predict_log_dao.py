# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from quant.common_tools.decorators import exc_time
from sqlalchemy import MetaData, select, and_
from quant.dao.data_source import dataSource
from sqlalchemy import Table
from quant.common_tools import datetime_utils
from sqlalchemy.sql import text
from quant.log.quant_logging import logger


class K_Data_60m_Predict_Log_Dao:

    @exc_time
    def insert(self, code, logistic_regression, random_forest_classifier, support_vector_classifier, xgb_classifier, sequantial_neural):
        sql = text('replace into k_data_60m_predict_log (date, code, '
                   'logistic_regression, '
                   'random_forest_classifier, '
                   'support_vector_classifier, '
                   'xgb_classifier, '
                   'sequantial_neural) '
                   'values(:date,:code,:logistic_regression,:random_forest_classifier,:support_vector_classifier,:xgb_classifier,:sequantial_neural)')

        result = dataSource.mysql_quant_conn.execute(sql, date=datetime_utils.get_current_date_hour(),
                                                     code=code,
                                                     logistic_regression=logistic_regression,
                                                     random_forest_classifier=random_forest_classifier,
                                                     support_vector_classifier=support_vector_classifier,
                                                     xgb_classifier=xgb_classifier,
                                                     sequantial_neural=sequantial_neural)

        return result


k_data_60m_predict_log_dao = K_Data_60m_Predict_Log_Dao()
