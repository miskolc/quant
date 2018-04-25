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

'''
 * 终极摆动指标
 * http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ultimate_oscillator

 * BP = Close - Minimum(Low or Prior Close).

 * TR = Maximum(High or Prior Close)  -  Minimum(Low or Prior Close)

 * Average7 = (7-period BP Sum) / (7-period TR Sum)
 * Average14 = (14-period BP Sum) / (14-period TR Sum)
 * Average28 = (28-period BP Sum) / (28-period TR Sum)

 * UO = 100 x [(4 x Average7)+(2 x Average14)+Average28]/(4+2+1)

'''

#
# df = ts.get_hist_data('600179', start='2018-01-01')
# print(df)
# Close = df['close'].head(1).values[0]
# Minimum = df['low'].head(1).values[0]
# Maximum = df['high'].head(1).values[0]
# BP = Close - Minimum
# TR = Maximum - Minimum
#
#
# def get_x_period_av(data, x):
#     return sum(data['close'][:x].values - data['low'][:x].values) / sum(data['high'][:x].values - data['low'][:x].values)
#
#
# av_7 = get_x_period_av(df, 7)
# av_14 = get_x_period_av(df, 14)
# av_28 = get_x_period_av(df, 28)
#
# UO_value = 100 * ((4 * av_7) + (2 * av_14) + av_28)/(4+2+1)
#
# print(UO_value)


