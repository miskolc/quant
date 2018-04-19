import tushare as ts
import numpy as np
from sqlalchemy import create_engine
# 导入futuquant api
import futuquant as ft

#df_sh = ts.get_hist_data('600179') #一次性获取全部日k线数据
#print(df_sh)

#df_now = ts.get_realtime_quotes("600179")
#df = ts.get_k_data('600179', ktype='5') #一次性获取全部日k线数据
#print(df)

#df_an = df_now.loc[df_now['code'] == '600179']

#print(df_now[['price']].values)

#print(df_now)

#df = ts.get_hist_data('600179') #一次性获取上证数据
#engine = create_engine('mysql://root:root@localhost/quantitative?charset=utf8')
#存入数据库
#df.to_sql('tick_data',engine,if_exists='append')

#print(df)
# 实例化行情上下文对象
'''
quote_ctx = ft.OpenQuoteContext(host="119.29.141.202", port=11111)
# 上下文控制
quote_ctx.start()              # 开启异步数据接收
quote_ctx.stop()               # 停止异步数据接收
quote_ctx.set_handler(handler) # 设置用于异步处理数据的回调对象

quote_ctx.get_stock_quote('600179')
'''

#df = ts.get_h_data('600000',start='2017-01-05',end='2017-01-09')
#print(df)

df_now = ts.get_realtime_quotes('600000')
print(df_now)