# ae.h - 2018/4/23
from app.dao.price_retrieval import price_retrieval_1min, price_retrieval_daily
import tushare as ts

if __name__ == '__main__':
    #price_retrieval_daily('600179', '2015-01-01', '2018-04-24', table_name='tick_data_daily')

    '''
    df = ts.get_hs300s()

    for code in df['code'].values:
        price_retrieval_daily(code, '2015-01-01', '2018-04-28',table_name='tick_data_daily')
        # price_retrieval_1min([code for code in np.array(df['code'].values)], '2015-01-01', '2018-04-23',
        #                      table_name='tick_data_1min_hs300')
    '''