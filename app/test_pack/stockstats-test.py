from stockstats import StockDataFrame
import tushare as ts
import pandas as pd



#Relative Strength Index
def RSI(df, n):
    i = 0
    UpI = [0]
    DoI = [0]
    while i + 1 <= len(df.index):
        UpMove = df.get_value(i + 1, 'high') - df.get_value(i, 'high')
        DoMove = df.get_value(i, 'low') - df.get_value(i + 1, 'low')
        if UpMove > DoMove and UpMove > 0:
            UpD = UpMove
        else: UpD = 0
        UpI.append(UpD)
        if DoMove > UpMove and DoMove > 0:
            DoD = DoMove
        else: DoD = 0
        DoI.append(DoD)
        i = i + 1
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
    PosDI = pd.Series(pd.ewma(UpI, span = n, min_periods = n - 1))
    NegDI = pd.Series(pd.ewma(DoI, span = n, min_periods = n - 1))
    RSI = pd.Series(PosDI / (PosDI + NegDI), name = 'RSI_' + str(n))
    df = df.join(RSI)
    return df

df = ts.get_k_data('600179')

stock = StockDataFrame.retype(df)

#print(stock.get('boll'))
#print(stock.get('boll_ub'))
print(stock['rsi_6'])

df = RSI(df, 6)
print(df)
#print(stock.get('macd'))
#print(stock.get('macds'))
#print(stock.get('macdh'))

