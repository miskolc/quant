# ae.h - 2018/4/23

import pandas as pd
from statsmodels.tsa.stattools import adfuller

from app.common_tools import decorators
from dao import data_source


@decorators.exc_time
def gmb_test(code):
    time_close_df = pd.read_sql_query(sql='select datetime,close from tick_data_1min_hs300 where code=\'%s\'' % code,
                                      con=data_source.create(), index_col='datetime')
    adf_result = list(adfuller(time_close_df['close']))
    print('\n')

    test_statics = adf_result[0]
    p_value = adf_result[1]
    critical_value_1 = adf_result[4]['1%']
    critical_value_5 = adf_result[4]['5%']
    critical_value_10 = adf_result[4]['10%']

    print('test statics: %s' % test_statics)
    print('p_value: %s' % p_value)
    print('critical value 1%%: %s' % critical_value_1)
    print('critical value 5%%: %s' % critical_value_5)
    print('critical value 10%%: %s' % critical_value_10)
