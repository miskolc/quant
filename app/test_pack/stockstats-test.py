from stockstats import StockDataFrame
import tushare as ts


df = ts.get_k_data('600179')

stock = StockDataFrame.retype(df)

print(stock.get('cci'))

#print(stock.get('macd'))
#print(stock.get('macds'))
#print(stock.get('macdh'))
