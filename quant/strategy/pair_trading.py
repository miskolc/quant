# coding=utf-8
# ae_h - 2018/6/1
import tushare as ts
from sqlalchemy import create_engine, MetaData

from app.common_tools.GBM_verify import gmb_test
from app.test_pack.pairs.hurst import hurst
from quant.config import config
from quant.dao import dataSource
from quant.dao.k_data_dao import k_data_dao
from quant.common_tools.datetime_utils import get_current_date
from quant.log.quant_logging import quant_logging
import pandas as pd
import numpy as np

# def pair_stock():
from quant.test import PROJECT_NAME


def init_db():
    default_config = config['default']

    # 如果配置DATABASE_QUANT_URI属性, 实例化mysql_quant_engine
    if default_config.DATABASE_QUANT_URI:
        # 使用单例模式保存数据库engine
        mysql_quant_engine = create_engine(default_config.DATABASE_QUANT_URI, encoding='utf8',
                                           convert_unicode=True, pool_size=10, pool_recycle=1200)
        dataSource.mysql_quant_engine = mysql_quant_engine
        dataSource.mysql_quant_conn = mysql_quant_engine.connect()
        dataSource.mysql_quant_metadata = MetaData(dataSource.mysql_quant_conn)


def init_logger():
    default_config = config['default']
    # 使用单例模式保存logger
    quant_logging.create_logger(default_config.DEBUG, PROJECT_NAME)


def before_run():
    init_logger()
    init_db()


def count_mean_std_plot(data, result_df):

    mean_v = float(data["close"].mean())
    data = {'mean': 1}
    serie = pd.Series(data)
    
    result_df['mean'] = serie
    # ddf['std'] = data["close"].std()
    # ddf['interregional_up'] = data["close"].mean() + data["close"].std()
    # ddf['interregional_down'] = data["close"].mean() - data["close"].std()
    # ddf['hurst_v'] = hurst(data['close'])
    #
    # result_df.append(ddf[['mean', 'std', 'interregional_up', 'interregional_down', 'hurst_v']])

    # print(ddf[['mean', 'std', 'interregional_up', 'interregional_down', 'hurst_v']])
    print(result_df)

if __name__ == '__main__':

    before_run()
    hs_300 = ts.get_hs300s()

    code_list = list(hs_300['code'])

    sql = "select * from k_data where `date`> '2017-01-01'"
    hs_df = pd.read_sql(sql=sql, con=dataSource.mysql_quant_conn, index_col=['date'])

    result_df = pd.DataFrame(columns=[''])

    for i in range(0, len(code_list)):
        for j in range(1, len(code_list)):
            stock1_code = code_list[i]
            stock2_code = code_list[j]

            quant_logging.logger.debug('code1 %s | code2 %s' % (stock1_code, stock2_code))
            df1 = hs_df[hs_df['code'] == stock1_code]
            df2 = hs_df[hs_df['code'] == stock2_code]

            df3 = pd.DataFrame(index=df1.index, columns=['close'])

            df3[stock1_code] = df1['close']
            df3[stock2_code] = df2['close']

            df3['close'] = df1['close'] / df2['close']
            df3.dropna()

            quant_logging.logger.debug('not paired') if hurst(df3["close"]) < 0.5 else count_mean_std_plot(df3, result_df)

    result_df.to_csv('result_df.csv')
