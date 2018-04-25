import pandas as pd


# 前N日平均涨跌幅
def fill(data, ndays):
    price_changes = pd.Series(pd.Series.rolling(data['price_change'], ndays).mean(), name='ma_price_change_%s' % ndays)
    data = data.join(price_changes)
    return data


