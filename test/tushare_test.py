# ae_h - 2018/7/20
import tushare as ts


df = ts.get_stock_basics()
df.to_csv('stock_basic.csv', encoding='utf-8')

