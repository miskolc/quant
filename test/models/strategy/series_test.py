# ae_h - 2018/6/8


import tushare as ts
from statsmodels.tsa.stattools import adfuller

from app.test_pack.pairs.hurst import hurst

df_s = ts.get_k_data('600179', start='2017-01-01')['close']

adf_result = list(adfuller(df_s))

hurst_v = hurst(df_s)

print(adf_result)

result_score = adf_result[0]

print('result score: %s' % result_score)

percent_1 = adf_result[4]['1%']
percent_5 = adf_result[4]['5%']
percent_10 = adf_result[4]['10%']

print('1: %s' % percent_1)
print('5 %s' % percent_5)
print('10 %s' % percent_10)

print(df_s.mean())
print(df_s.std())

print(df_s.mean()+df_s.std(), df_s.mean()-df_s.std())

print(hurst_v)
