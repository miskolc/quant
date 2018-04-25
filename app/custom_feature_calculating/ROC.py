import pandas as pd


# Rate of Change (ROC)/股票变动速率
def ROC(data, n):
    N = data['close'].diff(n)
    D = data['close'].shift(n)
    ROC = pd.Series(N / D, name='roc')
    data = data.join(ROC)
    return data
