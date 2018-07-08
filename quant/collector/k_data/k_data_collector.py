# -*- coding: UTF-8 -*-
# greg.chen - 2018/4/24

from datetime import datetime
import tushare as ts
from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
from quant.log.quant_logging import logger
from quant.dao.basic.stock_industry_dao import stock_industry_dao


# collect k_data from tushare and save into db
@exc_time
def collect_single(code, start, end, table_name='k_data'):
    try:
        data = ts.get_k_data(code, start=start, end=end)
        data['code'] = code
        data['pre_close'] = data['close'].shift(1)
        data = data.dropna()
        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        logger.error(e)


@exc_time
def collect_single_daily(code, table_name='k_data'):
    try:
        data = ts.get_k_data(code)
        data['code'] = code
        data['pre_close'] = data['close'].shift(1)
        data = data.tail(1)
        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        logger.error(e)


# 抓取沪深300所有K_data_daily数据
@exc_time
def collect_hs300_full(table_name='k_data'):
    df = ts.get_hs300s()
    now = datetime.now().strftime('%Y-%m-%d')
    for code in df['code'].values:
        collect_single(code=code, start='2015-01-01', end=now, table_name=table_name)



# 抓取沪深300每天K_data_daily数据
@exc_time
def collect_hs300_daily(table_name='k_data'):
    now = datetime.now().strftime('%Y-%m-%d')
    is_holiday = ts.is_holiday(now)
    # 如果是假日, 跳过
    if is_holiday:
        return

    df = ts.get_hs300s()
    for code in df['code'].values:
        collect_single_daily(code=code, table_name=table_name)

# 抓取所有k_data数据
@exc_time
def collect_all():
    now = datetime.now().strftime('%Y-%m-%d')
    df_industry = stock_industry_dao.get_list()
    for index,row in df_industry.iterrows():
        code = row['code']
        collect_single(code=code, start='2015-01-01', end=now)


# 抓取沪深每天K_data_daily数据
@exc_time
def collect_all_daily(table_name='k_data'):
    now = datetime.now().strftime('%Y-%m-%d')
    is_holiday = ts.is_holiday(now)
    # 如果是假日, 跳过
    if is_holiday:
        return

    df_industry = stock_industry_dao.get_list()
    for index,row in df_industry.iterrows():
        code = row['code']
        collect_single_daily(code=code, table_name=table_name)