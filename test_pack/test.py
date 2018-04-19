# ae.h - 2018/4/19
import tushare as ts
import pandas as pd
import numpy as np

# antong_df = ts.get_hist_data('600179')
#
# antong_df.to_csv('/Users/yw.h/Documents/antong_hist/antong_hist.csv', columns=[columns_name for columns_name in antong_df.columns])
#
# print(antong_df)

tick_code = '600179'
df = ts.get_hist_data(tick_code)  # 一次性获取上证数据
df = df.sort_index()


feature_list = ['y_open', 'ma5', 'ma10', 'ma20', 'ubb', 'lbb', 'cci', 'evm', 'ewma', 'fi']

# 1. 取出df中的特定feature.tail(1).values
# 2. 把对应特征的tail(1).values插入df.now<dataframe


for feature in feature_list:
    df