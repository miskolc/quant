# -*- coding: UTF-8 -*-
# greg.chen - 2018/4/24

from datetime import datetime, timedelta

import tushare as ts
from dao.data_source import dataSource
from log.quant_logging import logger

from common_tools import datetime_utils
from common_tools import exc_time


# collect k_data from tushare and save into db
@exc_time
def collect_single(code, table_name='k_data_60m', conn=None):

    try:
        data = ts.bar(conn=conn, code=code, freq='60min',
                      start_date='2015-01-01', retry_count=10)

        data.rename(columns={'vol': 'volume'}, inplace=True)
        data = data.drop(columns=['amount'])
        data['date'] = data.index
        data['pre_close'] = data['close'].shift(-1)
        data = data.dropna()
        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        logger.error("collect failed code:%s, exception:%s"% (code, repr(e)))



@exc_time
def collect_single_daily(code, table_name='k_data_60m', conn=None):
    start = (datetime.now() - timedelta(5)).strftime(datetime_utils.DATE_FORMAT)

    try:
        data = ts.bar(conn=conn, code=code, freq='60min',
                      start_date=start, retry_count=10)

        data.rename(columns={'vol': 'volume'}, inplace=True)
        data = data.drop(columns=['amount'])
        data['date'] = data.index
        data['pre_close'] = data['close'].shift(-1)
        data = data.dropna()
        data = data.head(4)
        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        logger.error("collect failed code:%s, exception:%s" % (code, repr(e)))


# 抓取沪深300所有K_data_60m数据
@exc_time
def collect_hs300_full():
    df = ts.get_hs300s()
    conn = ts.get_apis()
    #now = datetime.now().strftime('%Y-%m-%d')
    for code in df['code'].values:
        collect_single(code=code, conn=conn)

    ts.close_apis(conn)


# 抓取沪深300每天K_data_60m数据
@exc_time
def collect_hs300_daily():
    now = datetime.now().strftime('%Y-%m-%d')
    is_holiday = ts.is_holiday(now)
    # 如果是假日, 跳过
    if is_holiday:
        return

    conn = ts.get_apis()
    df = ts.get_hs300s()
    for code in df['code'].values:
        collect_single_daily(code=code, conn=conn)

    ts.close_apis(conn)
