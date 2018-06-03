# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

import os
import sys

# Append project path to system path
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

from quant.log.quant_logging import logger
from quant.config import default_config
from sqlalchemy import create_engine, MetaData
from quant.dao.data_source import dataSource
from quant.models.k_data import k_data_manage
import schedule

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



if __name__ == '__main__':
    init_db()

    k_data_manage.predict_k_data()

    #schedule.every().day.at("17:00").do(k_data_manage.training_k_data())

    '''
    while True:
        schedule.run_pending()
        time.sleep(1)
    '''
