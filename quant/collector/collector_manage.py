# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

import os
import sys

# Append project path to system path
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

from quant.log.quant_logging import quant_logging as logging
from quant.collector.config import config
from sqlalchemy import create_engine
import quant.collector.ts.k_data_collector as k_data
from quant.dao.data_source import dataSource
import schedule
import time

PROJECT_NAME = "quant-collector"

def init_db():
    default_config = config['default']

    # 如果配置DATABASE_QUANT_URI属性, 实例化mysql_quant_engine
    if default_config.DATABASE_QUANT_URI:
        # 使用单例模式保存数据库engine
        mysql_quant_engine = create_engine(default_config.DATABASE_QUANT_URI,encoding='utf8',
                                           convert_unicode=True, pool_size=100 , pool_recycle=1200)
        dataSource.mysql_quant_engine = mysql_quant_engine


def init_logger():
    default_config = config['default']
    # 使用单例模式保存logger
    logging.create_logger(default_config.DEBUG, PROJECT_NAME)


if __name__ == '__main__':
    init_logger()
    init_db()

    schedule.every().day.at("15:30").do(k_data.collect_hs300_daily)
    while True:
        schedule.run_pending()
        time.sleep(1)