#!/usr/bin/python
# -*- coding: utf-8 -*-

# price_retrieval.py 
# 

from __future__ import print_function

from datetime import datetime, timedelta

import tushare as ts

from app.common_tools import decorators
from quant.dao import data_source


# 爬取指数1min窗口数据
# code: 上证代码->'000001'
# freq: 1min/five_min

def index_retrieval(code, freq, start_date, end_date, table_name='tick_data_1min_sh'):
    conn = ts.get_apis()
    try:
        data = ts.bar(conn=conn, code=code, asset='INDEX', freq=freq,
                      start_date=start_date, end_date=end_date)
        data['code'] = 'sh'
        data.to_sql(table_name, data_source.create(), if_exists='append')
    except Exception as e:
        print(e)
    finally:
        ts.close_apis(conn)


# 爬取股票价格1min窗口数据
# code: '600179'
# freq: 1min
@decorators.exc_time
def price_retrieval_1min(code, start_date, end_date, table_name='tick_data_1min'):
    conn = ts.get_apis()
    try:
        data = ts.bar(conn=conn, code=code, freq='1min',
                      start_date=start_date, end_date=end_date)
        data.to_sql(table_name, data_source.create(), if_exists='append')
    except Exception as e:
        print(e)
    finally:
        ts.close_apis(conn)


# 爬取股票价格5min窗口数据
@decorators.exc_time
def price_retrieval_5min(code, start_date, end_date):
    conn = ts.get_apis()
    try:
        data = ts.bar(conn=conn, code=code, freq='5min',
                      start_date=start_date, end_date=end_date)
        data.to_sql('tick_data_5min', data_source.create(), if_exists='append')
    except Exception as e:
        print(e)
    finally:
        ts.close_apis(conn)
        print('end' + str(datetime.now()))


# 爬取股票价格30min窗口数据
@decorators.exc_time
def price_retrieval_30min(code, start_date, end_date):
    conn = ts.get_apis()
    try:
        data = ts.bar(conn=conn, code=code, freq='30min',
                      start_date=start_date, end_date=end_date)
        data.to_sql('tick_data_30min', data_source.create(), if_exists='append')
    except Exception as e:
        print(e)
    finally:
        ts.close_apis(conn)


# 爬取股票价格60min窗口数据
@decorators.exc_time
def price_retrieval_60min(code, start_date, end_date):
    conn = ts.get_apis()
    try:
        data = ts.bar(conn=conn, code=code, freq='60min',
                      start_date=start_date, end_date=end_date)
        data.to_sql('tick_data_60min', data_source.create(), if_exists='append')
    except Exception as e:
        print(e)
    finally:
        ts.close_apis(conn)


# 爬取每天股票价格
@decorators.exc_time
def price_retrieval_daily(code, start_date, end_date, table_name='tick_data'):
    try:
        data = ts.get_k_data(code=code, start=start_date, end=end_date)
        data['code'] = code
        data.to_sql(table_name, data_source.create(), if_exists='append', index=False)
    except Exception as e:
        print(e)

        # 爬取每天股票价格


@decorators.exc_time
def price_retrieval_tick_data(code, date, table_name='tick_data'):
    try:
        df = ts.get_tick_data('600179', date=date)
        df['code'] = code
        df['date'] = date + ' ' + df['time']
        df = df.drop(columns=['time'])
        df = df.replace(['--'], 0)
        print('date: %, count: %', (date, len(df.index)))
        df.to_sql(table_name, data_source.create(), if_exists='append', index=False)

    except Exception as e:
        print(e)


# 或取每天股票价格
@decorators.exc_time
def get_price_daily(code, start_date, end_date):
    try:
        data = ts.get_hist_data(code=code, start=start_date, end=end_date)
        data['code'] = code
    except Exception as e:
        print(e)


def price_retrieval_realtime_quotes(code, table_name='tick_data_rt'):
    try:
        df = ts.get_realtime_quotes(code)
        df['date'] = df['date'] + ' ' + df['time']
        df.to_sql(table_name, data_source.create(), if_exists='append', index=False)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    # 当前时间
    now = datetime.now()
    # 前一天
    pre = now - timedelta(days=1)
    # format date to string
    start = pre.strftime('%Y-%m-%d')
    end = now.strftime('%Y-%m-%d')
    print('start=%s,end=%s' % (start, end))

    price_retrieval_5min('600179', '2018-05-02', '2018-05-03')
    # index_retrieval('000001', '5min', '2016-01-01', '2018-04-26', table_name='tick_data_5min')
    # price retrieval
    # index_retrieval('000001', '1min', '2016-01-01', '2018-04-20')
    # price_retrieval('600179', '1min', '2016-01-01', '2018-04-20')
    # price_retrieval('600270', '1min', '2016-01-01', '2018-04-20')
    # price_retrieval('000725', '1min', '2016-01-01', '2018-04-20')