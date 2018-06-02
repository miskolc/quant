# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/21
from datetime import datetime, timedelta

import tushare as ts

from quant.common_tools.decorators import exc_time
from quant.crawler.yahoo_finance_api import yahoo_finance_api
from quant.dao.data_source import dataSource
from quant.log.quant_logging import logger

'''
    上证综合指数: 000001
    深证成份指数: 399001
    沪深300指数: 000300
    中证小盘500指数: 000905
    納斯達克指數: ^IXIC
    恒生指數: ^HSI
    标普500: ^GSPC
    道琼斯指数: ^DJI
'''


@exc_time
def collect_single_index_from_yahoo(code, start, end, table_name='index_k_data'):
    try:
        data = yahoo_finance_api.get_k_data(code, start_date=start, end_date=end)
        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        logger.error(e)


@exc_time
def collect_single_index_daliy_from_yahoo(code, table_name='index_k_data'):
    now = datetime.now().strftime('%Y-%m-%d')
    is_holiday = ts.is_holiday(now)
    # 如果是假日, 跳过
    if is_holiday:
        return

    try:
        start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        end = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

        data = yahoo_finance_api.get_k_data(code, start_date=start, end_date=end)
        data = data.tail(1)
        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        logger.error(e)


@exc_time
def collect_single_index_from_ts(code, start, end, table_name='index_k_data'):
    try:
        data = ts.get_k_data(code, start=start, end=end, index=True)
        data['code'] = code
        data['pre_close'] = data['close'].shift(1)
        data = data.dropna()
        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        logger.error(e)


@exc_time
def collect_single_index_daily_from_ts(code, table_name='index_k_data'):
    now = datetime.now().strftime('%Y-%m-%d')
    is_holiday = ts.is_holiday(now)
    # 如果是假日, 跳过
    if is_holiday:
        return

    try:
        data = ts.get_k_data(code, index=True)
        data['code'] = code
        data['pre_close'] = data['close'].shift(1)
        data = data.tail(1)
        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        logger.error(e)


# 每天爬取中国各类指数
@exc_time
def collect_index_china_daily():
    collect_single_index_daily_from_ts('000001')
    collect_single_index_daily_from_ts('399001')
    collect_single_index_daily_from_ts('000300')
    collect_single_index_daily_from_ts('000905')


# 每天爬取香港各类指数
@exc_time
def collect_index_hk_daily():
    collect_single_index_daliy_from_yahoo('^HSI')


# 每天爬取USA各类指数
@exc_time
def collect_index_usa_daily():
    collect_single_index_daliy_from_yahoo('^HSI')
    collect_single_index_daliy_from_yahoo('^IXIC')
    collect_single_index_daliy_from_yahoo('^GSPC')
    collect_single_index_daliy_from_yahoo('^DJI')
