# ae.h - 2018/5/20
import talib
import tushare as ts
import pandas as pd
import numpy as np
from talib import abstract

df = ts.get_k_data('600179', ktype='D', start='2015-01-01')

# df_slice = df.tail(5)

# ema = abstract.Function('ema')

bbands = abstract.Function('bbands')

# ema_value = ema(df, timeperiod=5, price='close')

bbands_value = bbands(df, 20, 2, 2)

# print(df_slice)

# print(ema_value)
print(bbands_value)
