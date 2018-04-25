# ae.h - 2018/4/19
import functools
import tushare as ts
import pandas as pd
import numpy as np
from yahoo_finance import Share
import datetime
import pandas_datareader.data as web
import futuquant as ft
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt

# tick_df = pd.DataFrame()
# df = ts.get_hist_data('600179')
# for date in df.index.values:
#     tick_df.append(ts.get_tick_data('600179', date=date, pause=5))
#
# print(tick_df)


# df = ts.get_tick_data('600179', date='2016-04-21', pause=5)
# print(df)



# df = ts.get_tick_data('600179', date='2018-04-23', pause=5)

# print(df)

# df = pd.read_csv('600179tick0423')
# # print(df)
#
#
# # df = df.drop_duplicates(['time'])
# # df = df.drop_duplicates(['price'])
# # df = df.reset_index()
#
#
# # df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S')
# # print(df['time'].values)
# x = df['time'].values
# y = df['price'].values
#
# # print(x)
# # print(y)
# #
# plt.figure(figsize=(20,10))
# plt.plot(x, y)
# # plt.xticks(rotation=70)
# plt.xlabel('time')
# plt.ylabel('price')
# plt.show()
