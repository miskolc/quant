# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/21
from datetime import datetime, timedelta

import tushare as ts

from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
from quant.log.quant_logging import logger
from quant.common_tools import datetime_utils

'''
    上证综合指数: 000001
    深证成份指数: 399001
    沪深300指数: 000300
    中证小盘500指数: 000905
'''


@exc_time
def collect_single_index_from_ts(code, table_name='index_k_data_60m', conn=None):
    try:
        data = ts.bar(conn=conn, code=code, freq='60min', asset="INDEX",
                      start_date='2016-01-01', retry_count=10)

        data.rename(columns={'vol': 'volume'}, inplace=True)
        data = data.drop(columns=['amount'])
        data['date'] = data.index
        data['pre_close'] = data['close'].shift(-1)
        data = data.dropna()

        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        logger.error(e)


@exc_time
def collect_single_index_daily_from_ts(code, table_name='index_k_data_60m', conn=None):
    start = (datetime.now() - timedelta(5)).strftime(datetime_utils.DATE_FORMAT)

    try:
        data = ts.bar(conn=conn, code=code, freq='60min', asset="INDEX",
                      start_date=start, retry_count=10)

        data.rename(columns={'vol': 'volume'}, inplace=True)
        data = data.drop(columns=['amount'])
        data['date'] = data.index
        data['pre_close'] = data['close'].shift(-1)
        data = data.head(4)
        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        logger.error(e)


# 全量爬取中国各类指数
@exc_time
def collect_index_china_full():
    conn = ts.get_apis()
    collect_single_index_from_ts('000001', conn=conn)
    collect_single_index_from_ts('399001', conn=conn)
    collect_single_index_from_ts('000300', conn=conn)
    collect_single_index_from_ts('000905', conn=conn)
    ts.close_apis(conn)


# 每天爬取中国各类指数
@exc_time
def collect_index_china_daily():
    now = datetime.now().strftime('%Y-%m-%d')
    is_holiday = ts.is_holiday(now)
    # 如果是假日, 跳过
    if is_holiday:
        return

    conn = ts.get_apis()

    collect_single_index_daily_from_ts('000001', conn=conn)
    collect_single_index_daily_from_ts('399001', conn=conn)
    collect_single_index_daily_from_ts('000300', conn=conn)
    collect_single_index_daily_from_ts('000905', conn=conn)

    ts.close_apis(conn)