import talib
import tushare as ts
import pandas as pd


'''
强弱指标理论认为，任何市价的大涨或大跌，均在0-100之间变动，根据常态分配，认为RSI值多在30-70之间变动，
通常80甚至90时被认为市场已到达超买状态，至此市场价格自然会回落调整。当价格低跌至30以下即被认为是超卖状态，市价将出现反弹回升

时间周期:6,12,24
'''
def fill(df, col="close"):
    rsi6 = pd.Series(talib.RSI(df[col], timeperiod=6), name="rsi6")

    rsi12 = pd.Series(talib.RSI(df[col], timeperiod=12), name="rsi12")
    rsi24 = pd.Series(talib.RSI(df[col], timeperiod=24), name="rsi24")

    df = df.join(rsi6)
    df = df.join(rsi12)
    df = df.join(rsi24)
    return df


if __name__ == "__main__":
    df = ts.get_k_data('600179')

    df = fill(df)
    print(df)
