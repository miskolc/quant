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

#df_now = ts.get_realtime_quotes('600000')
#print(df_now)

#获取上证指数k线数据
#df_sh = ts.get_hist_data('511880', start='2017-01-01', end='2018-01-01')
#print(df_sh)
#print(((df_sh['close']-df_sh['low'])/df_sh['low']).values.sum())
#df_sh=ts.bar(conn=ts.get_apis(), code='000001',freq='five_min', start_date='2017-01-18', end_date='2017-02-18')
#df_sh = ts.get_k_data('sh', ktype='5',start='2017-01-05')


#df_sh = ts.get_k_data('sh')
#000001
#df_sh=ts.bar(conn=ts.get_apis(), code='000001.sh',freq='1min', start_date='2018-01-18', end_date='2018-02-18')
#print(df_sh.tail(1))

#df_sh=ts.bar(conn=ts.get_apis(), code='000001',asset='INDEX',freq='1min', start_date='2016-01-01', end_date='2018-04-20')
#engine = create_engine('mysql://root:root@localhost/quantitative?charset=utf8')
#df_sh.to_sql('tick_data_1',engine,if_exists='append')
#print(df_sh.tail(1))

#df = ts.get_realtime_quotes('600179') #Single stock symbol
#print(df.head(10))

# codes = ['600009', '600085', '600196', '600406', '600522', '600547', '600585',
#          '600685', '601009', '601012', '601601', '601607',
#          '601878', '601888', '000413', '000728', '000858',
#          '001979', '002024', '002146', '002230', '002310',
#          '002411', '002415', '002450', '002460', '002470',
#          '002714', '002831', '300070', '300072']

codes = ['600036', '600153', '600276', '600690', '601318', '601888', '601958', '000895', '300136']


'''
list = []
for code in codes:
    df_sh = ts.get_hist_data(code)

    if df_sh is None:
        continue

    date = df_sh.index.values[0]
    if date < '2018-05-03':
        continue

    close = df_sh["close"].head(1).values[0]
    ma5 = df_sh["ma5"].head(1).values[0]
    ma10 = df_sh["ma10"].head(1).values[0]
    ma20 = df_sh["ma20"].head(1).values[0]
    if close > ma5 and close > ma10 and close > ma20:
        list.append(code)


p_change_list=[]
for code in codes:
    df = ts.get_realtime_quotes(code)

    df['p_change'] = (float(df['price']) - float(df['pre_close'])) / float(df['pre_close'])

    p_change = df['p_change'].head(1).values[0]

    print(code, p_change)
    p_change_list.append(p_change)

print(len(codes))


print("%.4f" % (sum(p_change_list)/len(codes)))
'''

'''
df_sh=ts.bar(conn=ts.get_apis(), code='000001',freq='60min', start_date='2015-06-01')
df_sh['date'] = df_sh.index
print(df_sh)
print(df_sh.columns.values)
print(df_sh[["vol",'open','close']])
'''

'''
df_sh = ts.bar(conn=ts.get_apis(), code='XAUUSD',freq='X', start_date='2018-01-08', factors=[ 'tor'])
print(df_sh)



df_sz50 = ts.get_sz50s()
df_zz = ts.get_zz500s()
print(df_sz50)
'''

df_sh = ts.bar(conn=ts.get_apis(), code='601398', factors=[ 'tor'])
print(df_sh)


#df_now = ts.get_realtime_quotes('601398')
#print(df_now)

'''

df = ts.bar('^GSPC', conn=ts.get_apis(), asset='X', start_date='2016-01-01')
print(df)
'''