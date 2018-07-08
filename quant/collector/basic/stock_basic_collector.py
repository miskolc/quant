# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/06

from quant.common_tools.decorators import exc_time
from quant.crawler.east_money_api import east_money_api
from quant.dao.basic.stock_industry_dao import stock_industry_dao
from quant.dao.basic.stock_basic_dao import stock_basic_dao
from quant.dao.data_source import dataSource
from quant.log.quant_logging import logger

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

    df_industry = stock_industry_dao.get_list()
    for index, row in df_industry.iterrows():
        code = row['code']
        df = east_money_api.get_stock_basic(code)
        try:

            df.to_sql('stock_basic', dataSource.mysql_quant_engine, if_exists='append', index=False)
        except Exception as e:

            logger.error("code:%s, error:%s" %(code, repr(e)))