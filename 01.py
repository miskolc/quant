import tushare as ts
import numpy as np
from sqlalchemy import create_engine

#df_sh = ts.get_hist_data('600179') #一次性获取全部日k线数据
#print(df_sh)

df_now = ts.get_realtime_quotes("600179")
print(df_now)

#df_an = df_now.loc[df_now['code'] == '600179']

#print(df_now[['price']].values)

#print(df_now)

#df = ts.get_hist_data('600179') #一次性获取上证数据
#engine = create_engine('mysql://root:root@localhost/quantitative?charset=utf8')
#存入数据库
#df.to_sql('tick_data',engine,if_exists='append')

#print(df)

data2 = [[1,2,3,4], [5,6,7,8]]
arr2 = np.array(data2)
print(arr2[0:][0])