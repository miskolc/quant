# -*- coding: UTF-8 -*-
# greg.chen - 2018/4/24

from datetime import datetime

import tushare as ts

from common_tools.datetime_utils import get_current_date
from config import default_config
from dao.basic.stock_industry_dao import stock_industry_dao
from dao.basic.trade_date_dao import trade_date_dao
from dao.data_source import dataSource
from dao.k_data import fill_market
from log.quant_logging import logger

from common_tools.decorators import exc_time

INDEX_CODES = ['SH.000300', 'SH.000001']

# collect k_data from tushare and save into db
@exc_time
def collect_single(code, start, end, futu_quote_ctx):
    table_name = 'k_data'
    try:
        state, data = futu_quote_ctx.get_history_kline(fill_market(code), ktype='K_DAY', autype='qfq', start=start,
                                                       end=end)
        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        logger.error(e)


@exc_time
def collect_single_daily(code, futu_quote_ctx, start=None, end=None):
    table_name = 'k_data'

    if start is None:
        start = get_current_date()

    if end is None:
        end = get_current_date()

    try:
        state, data = futu_quote_ctx.get_history_kline(fill_market(code), ktype='K_DAY', autype='qfq', start=start, end=end)
        data = data.tail(1)
        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        logger.error(e)



# 抓取所有k_data数据
@exc_time
def collect_all(futu_quote_ctx):
    now = datetime.now().strftime('%Y-%m-%d')
    df_industry = stock_industry_dao.get_stock_code_list()
    for index,row in df_industry.iterrows():
        code = row['code']
        collect_single(code=code, start='2013-01-01', end=now, futu_quote_ctx=futu_quote_ctx)


# 抓取所有k_data数据
@exc_time
def collect_all_index(futu_quote_ctx):
    now = datetime.now().strftime('%Y-%m-%d')
    is_holiday = trade_date_dao.is_holiday(now)
    # 如果是假日, 跳过
    if is_holiday:
        return

    for code in INDEX_CODES:
        collect_single(code=code, start='2013-01-01', end=now, futu_quote_ctx=futu_quote_ctx)



# 抓取每天K_data数据
@exc_time
def collect_all_daily(futu_quote_ctx):
    now = datetime.now().strftime('%Y-%m-%d')
    is_holiday = trade_date_dao.is_holiday(now)
    # 如果是假日, 跳过
    if is_holiday:
        return

    df_industry = stock_industry_dao.get_stock_code_list()
    for index,row in df_industry.iterrows():
        code = row['code']
        collect_single_daily(code=code, futu_quote_ctx=futu_quote_ctx)


# 抓取每天K_data数据
@exc_time
def collect_all_index_daily(futu_quote_ctx):
    now = datetime.now().strftime('%Y-%m-%d')
    is_holiday = trade_date_dao.is_holiday(now)
    # 如果是假日, 跳过
    if is_holiday:
        return

    for code in INDEX_CODES:
        collect_single_daily(code=code, futu_quote_ctx=futu_quote_ctx)