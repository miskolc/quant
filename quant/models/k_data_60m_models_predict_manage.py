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
from quant.models.k_data_60m import k_data_60m_manage
import warnings
from datetime import datetime
import tushare as ts


def init_db():
    # 如果配置DATABASE_QUANT_URI属性, 实例化mysql_quant_engine
    if default_config.DATABASE_QUANT_URI:
        # 使用单例模式保存数据库engine
        mysql_quant_engine = create_engine(default_config.DATABASE_QUANT_URI, encoding='utf8',
                                           convert_unicode=True, pool_size=100, pool_recycle=1200)
        dataSource.mysql_quant_engine = mysql_quant_engine
        dataSource.mysql_quant_conn = mysql_quant_engine.connect()
        dataSource.mysql_quant_metadata = MetaData(dataSource.mysql_quant_conn)


def predict():
    now = datetime.now().strftime('%Y-%m-%d')
    is_holiday = ts.is_holiday(now)
    # 如果是假日, 跳过
    if is_holiday:
        return

    k_data_60m_manage.predict_k_data()


if __name__ == '__main__':
    warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

    init_db()
    predict()
