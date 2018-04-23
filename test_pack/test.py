# ae.h - 2018/4/19
import functools
import tushare as ts
import pandas as pd
import numpy as np
from yahoo_finance import Share
import datetime
import pandas_datareader.data as web
import futuquant as ft


# antong_df = ts.get_hist_data('600179')
#
# antong_df.to_csv('/Users/yw.h/Documents/antong_hist/antong_hist.csv', columns=[columns_name for columns_name in antong_df.columns])
#
# print(antong_df)
#
# tick_code = '600179'
# df = ts.get_hist_data(tick_code)  # 一次性获取上证数据
# df = df.sort_index()
#
#
# feature_list = ['y_open', 'ma5', 'ma10', 'ma20', 'ubb', 'lbb', 'cci', 'evm', 'ewma', 'fi']


# start = datetime.datetime(2010, 1, 1)
# end = datetime.date.today()
#
# prices = web.DataReader("600179.SS", start, end)
# print(prices)
# quote_ctx = ft.OpenQuoteContext(host="127.0.0.1", port=11111)
# quote_ctx.start()
#
# quote_ctx.get_trading_days('SH', start_date=None, end_date=None)  # 获取交易日
# quote_ctx.get_stock_basicinfo('SH', stock_type='STOCK')           # 获取股票信息
# quote_ctx.get_history_kline('SH.600179', start=None, end=None, ktype='K_DAY', autype='qfq')  # 获取历史K线
# # quote_ctx.get_autype_list(code_list)      # 获取复权因子
# quote_ctx.get_market_snapshot(code_list)  # 获取市场快照
# quote_ctx.get_plate_list(market, plate_class)        #获取板块集合下的子板块列表
# quote_ctx.get_plate_stock(market, stock_code)        #获取板块下的股票列表


