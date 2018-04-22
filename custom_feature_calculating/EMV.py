import pandas as pd


# EMV Ease of Movement - 简易波动指标
def EVM(data, ndays):
    dm = ((data['high'] + data['low']) / 2) - ((data['high'].shift(1) + data['low'].shift(1)) / 2)
    br = (data['volume'] / 100000000) / ((data['high'] - data['low']))
    EVM = dm / br
    EVM_MA = pd.Series(pd.Series.rolling(EVM, ndays).mean(), name='evm')
    data = data.join(EVM_MA)
    return data
