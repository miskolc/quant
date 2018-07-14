# ae_h - 2018/7/8
import pandas as pd
import numpy as np


def acc_SMA(data, N):
    sma_v = pd.Series(index=data.index)
    last = np.nan
    for key in data.index:
        x = data[key]
        if last == last:
            x1 = (x + (N - 1) * last) / N
        else:
            x1 = x
        last = x1
        sma_v[key] = x1
        if x1 != x1:
            last = x
    return sma_v
