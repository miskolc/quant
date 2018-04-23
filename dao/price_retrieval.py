#!/usr/bin/python
# -*- coding: utf-8 -*-

# price_retrieval.py 
# 

from __future__ import print_function


from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
from sqlalchemy import create_engine
import tushare as ts
from datetime import datetime, timedelta
from dao import engine

# 爬取指数1min窗口数据
# code: 上证代码->'000001'
# freq: 1min/5min
def index_retrieval(code, freq, start_date, end_date):
    conn = ts.get_apis()
    try:
        data=ts.bar(conn=conn, code=code,asset='INDEX',freq=freq, 
        start_date=start_date, end_date=end_date)
        data.to_sql('tick_data_1min',engine.create(),if_exists='append')
    except Exception as e:
        print(e)
    finally:
        ts.close_apis(conn)

# 爬取股票价格1min窗口数据
# code: '600179'
# freq: 1min
def price_retrieval_1min(code, start_date, end_date):
    conn = ts.get_apis()
    try:
        data=ts.bar(conn=conn, code=code,freq='1min',
        start_date=start_date, end_date=end_date)
        data.to_sql('tick_data_1min',engine.create(),if_exists='append')
    except Exception as e:
        print(e)
    finally:
        ts.close_apis(conn) 

# 爬取股票价格5min窗口数据
def price_retrieval_5min(code, start_date, end_date):
    conn = ts.get_apis()
    try:
        data=ts.bar(conn=conn, code=code,freq='5min',
        start_date=start_date, end_date=end_date)
        data.to_sql('tick_data_5min',engine.create(),if_exists='append')
    except Exception as e:
        print(e)
    finally:
        ts.close_apis(conn)

# 爬取股票价格30min窗口数据
def price_retrieval_30min(code, start_date, end_date):
    conn = ts.get_apis()
    try:
        data=ts.bar(conn=conn, code=code,freq='30min',
        start_date=start_date, end_date=end_date)
        data.to_sql('tick_data_30min',engine.create(),if_exists='append')
    except Exception as e:
        print(e)
    finally:
        ts.close_apis(conn)

# 爬取股票价格60min窗口数据
def price_retrieval_60min(code, start_date, end_date):
    conn = ts.get_apis()
    try:
        data=ts.bar(conn=conn, code=code,freq='60min',
        start_date=start_date, end_date=end_date)
        data.to_sql('tick_data_60min',engine.create(),if_exists='append')
    except Exception as e:
        print(e)
    finally:
        ts.close_apis(conn)


# 爬取每天股票价格
def price_retrieval_daily(code, start_date, end_date):

    try:
        data=ts.get_hist_data(code=code,start=start_date, end=end_date)
        data['code'] = code
        data.to_sql('tick_data',engine.create(),if_exists='append')
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



    # price retrieval
    #index_retrieval('000001', '1min', '2016-01-01', '2018-04-20')
    #price_retrieval('600179', '1min', '2016-01-01', '2018-04-20')
    #price_retrieval('600270', '1min', '2016-01-01', '2018-04-20')
    #price_retrieval('000725', '1min', '2016-01-01', '2018-04-20')


