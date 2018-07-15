# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from common_tools.decorators import exc_time
from sqlalchemy import MetaData, select, and_
from dao.data_source import dataSource
from sqlalchemy import Table
from common_tools import datetime_utils
from sqlalchemy.sql import text
from log.quant_logging import logger


class K_Data_Model_Log_Dao:
    @exc_time
    def exists(self, code):
        # 绑定引擎
        # 连接数据表
        table = Table('k_data_model_log', dataSource.mysql_quant_metadata, autoload=True)
        s = select([table.c.code, table.c.date]) \
            .where(and_(table.c.date == datetime_utils.get_current_date(), table.c.code == code))

        result = dataSource.mysql_quant_conn.execute(s)
        logger.debug("row count:%s" % result.rowcount)
        return result.rowcount > 0

    @exc_time
    def insert(self, code, name, best_estimator, train_score, test_score, desc=None):
        sql = text('replace into k_data_model_log (date, code, name, best_estimator, train_score, test_score, `desc`) '
                   'VALUES(:date,:code,:name,:best_estimator,:train_score,:test_score,:desc)')

        result = dataSource.mysql_quant_conn.execute(sql, date=datetime_utils.get_current_date(),
                                                     code=code, name=name, best_estimator=best_estimator
                                                     , train_score=train_score, test_score=test_score, desc=desc)

        return result


k_data_model_log_dao = K_Data_Model_Log_Dao()
