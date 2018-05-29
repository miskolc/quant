# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

from quant.common_tools.decorators import exc_time
from sqlalchemy import MetaData
from quant.dao.data_source import dataSource
from sqlalchemy import Table


class K_Data_Model_Log_Dao:

    @exc_time
    def insert(self, code, name, best_estimator, train_score, test_score):

        conn = dataSource.mysql_quant_engine.connect()
        # 绑定引擎
        metadata = MetaData(dataSource.mysql_quant_engine)
        # 连接数据表
        k_data_model_log_table = Table('k_data_model_log', metadata, autoload=True)
        # 创建 insert 对象
        ins = k_data_model_log_table.insert()
        # 绑定要插入的数据
        ins = ins.values(code=code, name=name,
                        best_estimator=best_estimator,
                         train_score=train_score,
                         test_score=test_score)

        # 执行语句
        result = conn.execute(ins)

        return result


k_data_model_log_dao = K_Data_Model_Log_Dao()

