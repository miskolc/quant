# # ae_h - 2018/6/4
#
# import pandas as pd
import tushare as ts
# import matplotlib.pyplot as plt
# import numpy as np
#
#
# df = pd.read_csv('/Users/yw.h/Desktop/601118close.csv')
#
# open_price = df['open']
# high_price = df['high']
# low_price = df['low']
# close_price = df['close']
# pre_price = df['pre_close']
#
# min_slide_point = 3.2
# max_slide_point = 10.5
#
# plt.plot(open_price+5, label='open')
# plt.plot(high_price+2, label='high')
# plt.plot(pre_price, label='pre')
# plt.plot(low_price-2, label='low')
# plt.plot(close_price-5, label='close')
# plt.axhline(min_slide_point, linestyle='-')
# plt.axhline(max_slide_point, linestyle='-')
#
# y_ticks = np.arange(min_slide_point, max_slide_point)
# plt.yticks(y_ticks)
# plt.title('601118')
#
#
# plt.legend()
#
# plt.savefig()
# plt.show()
#
# # plt.title(code1 + '/' + code2)
# # plt.plot(res, label='res')
# # plt.axhline(res.mean(), linestyle='--', color='blue')
# # plt.legend()
# # plt.savefig('result.png')


from feature_utils.momentum_indicators import acc_SMA, acc_kdj

df = ts.get_k_data('000651', start='2015-01-01', end='2018-07-06')

