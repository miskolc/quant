import pandas as pd
import tushare as ts
import talib

# Rate of Change (ROC)
'''
 * 股票变动速率
    ROC是由当天的股价与一定的天数之前的某一天股价比较，其变动速度的大小,来反映股票市场变动的快慢程度。
    大多数的书籍上把ROC叫做变动速度指标、变动率指标或变化速率指标
'''

def ROC(data, n):
    N = data['close'].diff(n)
    D = data['close'].shift(n)
    ROC = pd.Series(N / D, name='roc')
    data = data.join(ROC)
    return data


def fill(df, n=10, col="close"):
    real = talib.ROC(df[col], n)
    roc = pd.Series(real, name='roc')
    df = df.join(roc)
    return df


if __name__ == "__main__":
    df = ts.get_k_data('600179')

    df = fill(df)

    print(df)
