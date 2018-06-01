# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from quant.common_tools.decorators import exc_time
from sqlalchemy import MetaData, select, and_
from quant.dao.data_source import dataSource
from sqlalchemy import Table
from quant.common_tools import datetime_utils
from sqlalchemy.sql import text
from quant.log.quant_logging import quant_logging as logging


class K_Data_Model_Log_Dao:
    @exc_time
    def exists(self, code):
        # 绑定引擎
        # 连接数据表
        table = Table('k_data_model_log', dataSource.mysql_quant_metadata, autoload=True)
        s = select([table.c.code, table.c.date]) \
            .where(and_(table.c.date == datetime_utils.get_current_date(), table.c.code == code))

        result = dataSource.mysql_quant_conn.execute(s)
        logging.logger.debug("row count:%s" % result.rowcount)
        return result.rowcount > 0

    @exc_time
    def insert(self, code, name, best_estimator, train_score, test_score, desc=None):

        # 连接数据表
        k_data_model_log_table = Table('k_data_model_log', dataSource.mysql_quant_metadata, autoload=True)

        # 创建 insert 对象
        ins = k_data_model_log_table.insert()
        # 绑定要插入的数据
        ins = ins.values(code=code, date=datetime_utils.get_current_date(), name=name,
                         best_estimator=best_estimator,
                         train_score=train_score,
                         test_score=test_score, desc=desc)

        # 执行语句
        result = dataSource.mysql_quant_conn.execute(ins)

        return result


k_data_model_log_dao = K_Data_Model_Log_Dao()
