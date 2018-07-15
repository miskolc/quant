# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/06

from common_tools.decorators import exc_time
from crawler.east_money_api import east_money_api
from dao.basic.stock_pool_dao import stock_pool_dao
from dao.basic.stock_basic_dao import stock_basic_dao
from dao.data_source import dataSource
from log.quant_logging import logger

'''
    pe,市盈率
    pb,市净率
    eps,每股收益
    roe,净资产收益率(%)
    profits_yoy,净利润同比(%)
    income_yoy, 营收同比(%)
    report_date,发布日期
'''


@exc_time
def collect_stock_basic():
    stock_basic_dao.truncate()

    df_pool = stock_pool_dao.get_list()
    for index, row in df_pool.iterrows():
        code = row['code']
        df = east_money_api.get_stock_basic(code[3:])
        try:

            df.to_sql('stock_basic', dataSource.mysql_quant_engine, if_exists='append', index=False)
        except Exception as e:

            logger.error("code:%s, error:%s" %(code, repr(e)))