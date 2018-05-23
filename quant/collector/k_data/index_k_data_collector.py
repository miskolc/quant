# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/21
import tushare as ts
from quant.common_tools.decorators import exc_time
from quant.dao.data_source import dataSource
from quant.log.quant_logging import quant_logging as logging
from quant.collector.util.yahoo_finance_api import yahoo_finance_api
from datetime import datetime

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
        logging.logger.error(e)


@exc_time
def collect_single_index_daliy_from_yahoo(code, table_name='index_k_data'):
    now = datetime.now().strftime('%Y-%m-%d')
    is_holiday = ts.is_holiday(now)
    # 如果是假日, 跳过
    if is_holiday:
        return

    try:
        delta = datetime.timedelta(days=-30)
        start = delta.strftime('%Y-%m-%d')
        end = now

        data = yahoo_finance_api.get_k_data(code, start=start, end=end)
        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        logging.logger.error(e)


@exc_time
def collect_single_index_from_ts(code, start, end, table_name='index_k_data'):
    try:
        data = ts.get_k_data(code, start=start, end=end, index=True)
        data['code'] = code
        data['pre_close'] = data['close'].shift(1)
        data = data.dropna()
        data.to_sql(table_name, dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        logging.logger.error(e)


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
        logging.logger.error(e)


# 爬取全量各类指数
@exc_time
def collect_sh_index_full():
    start = '2015-01-01'
    end = datetime.now().strftime('%Y-%m-%d')

    collect_single_index_from_ts('000001', start, end)
    collect_single_index_from_ts('399001', start, end)
    collect_single_index_from_ts('000300', start, end)
    collect_single_index_from_ts('000905', start, end)

    collect_single_index_from_yahoo("^HSI", start, end)
    collect_single_index_from_yahoo("^IXIC", start, end)
    collect_single_index_from_yahoo("^GSPC", start, end)
    collect_single_index_from_yahoo("^DJI", start, end)


# 爬取每日各类指数
@exc_time
def collect_index_daily():
    collect_single_index_daily_from_ts('000001')
    collect_single_index_daily_from_ts('399001')
    collect_single_index_daily_from_ts('000300')
    collect_single_index_daily_from_ts('000905')

    collect_single_index_daliy_from_yahoo('^HSI')
    collect_single_index_daliy_from_yahoo('^IXIC')
    collect_single_index_daliy_from_yahoo('^GSPC')
    collect_single_index_daliy_from_yahoo('^DJI')
