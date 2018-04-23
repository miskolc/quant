# ae.h - 2018/4/23
from dao.price_retrieval import price_retrieval_1min
import tushare as ts
import numpy as np

if __name__ == '__main__':
    df = ts.get_hs300s()

    for code in df['code'].values:
        price_retrieval_1min(code, '2015-01-01', '2018-04-23',table_name='tick_data_1min_hs300')
        # price_retrieval_1min([code for code in np.array(df['code'].values)], '2015-01-01', '2018-04-23',
        #                      table_name='tick_data_1min_hs300')
