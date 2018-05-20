from collector.collector_logging import collector_logging as logging
from collector.config import config
from sqlalchemy import create_engine

import collector.ts.k_data_collector as k_data
from dao.data_source import dataSource


def init_db():
    default_config = config['default']

    # 如果配置DATABASE_QUANT_URI属性, 实例化mysql_quant_engine
    if default_config.DATABASE_QUANT_URI:
        # 使用单例模式保存数据库engine
        mysql_quant_engine = create_engine(
            default_config.DATABASE_QUANT_URI,
            encoding='utf8', convert_unicode=True)

        dataSource.mysql_quant_engine = mysql_quant_engine


def init_logger():
    default_config = config['default']
    PROJECT_NAME = "quant-collector"
    logging.create_logger(default_config.DEBUG, PROJECT_NAME)


if __name__ == '__main__':

    # logger = init_logger("quant_collector")
    init_logger();
    init_db();
    k_data.collect('600179', start='2015-01-01', end='2018-05-19')

