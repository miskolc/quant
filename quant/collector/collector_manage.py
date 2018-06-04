# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

import os
import sys

# Append project path to system path
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

from quant.config import default_config
from sqlalchemy import create_engine, MetaData
import quant.collector.k_data.k_data_collector as k_data
import quant.collector.k_data_60m.k_data_60m_collector as k_data_60m
import quant.collector.k_data_60m.index_k_data_60m_collector as index_k_data_60m
import quant.collector.k_data.k_data_technical_feature_collector as k_data_feature_collector
import quant.collector.k_data.index_k_data_collector as index_k_data
from quant.dao.data_source import dataSource
import schedule
import time

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

    #feature_collector.collect_hs300_full()
    #k_data_60m.collect_hs300_full()
    #index_k_data_60m.collect_index_china_daily()

    schedule.every().day.at("15:30").do(k_data_60m.collect_hs300_daily)
    schedule.every().day.at("15:30").do(k_data.collect_hs300_daily)
    schedule.every().day.at("15:32").do(index_k_data.collect_index_china_daily)
    schedule.every().day.at("15:32").do(index_k_data_60m.collect_index_china_daily)

    schedule.every().day.at("15:35").do(k_data_feature_collector.collect_hs300_daily)
    schedule.every().day.at("16:30").do(index_k_data.collect_index_hk_daily)
    schedule.every().day.at("8:30").do(index_k_data.collect_index_usa_daily)

    while True:
        schedule.run_pending()
        time.sleep(1)
