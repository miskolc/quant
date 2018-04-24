# ae.h - 2018/4/23

import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from dao import engine
from common_tools.GBM_verify import gmb_test


#code_df = pd.read_sql_query('SELECT DISTINCT code from tick_data_1min_hs300', engine.create())




# for code in code_df['code']:
#     time_close_df = pd.read_sql_query('select datetime,close from tick_data_1min_hs300 where code=\'%s\'' % code)


#time_close_df = pd.read_sql_query('select datetime,close from tick_data_1min_hs300 where code=\'600436\'', engine.create(), index_col='datetime')

# time_close_df['datetime'] = pd.to_datetime(time_close_df['datetime'])
# time_close_df['datetime'] = time_close_df['datetime'].astype('datetime64[ns]')


#print(adfuller(time_close_df['close']))
# print(time_close_df)

gmb_test('600179')