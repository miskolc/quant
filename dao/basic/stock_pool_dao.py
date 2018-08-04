# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/7
import copy
import traceback

from common_tools.datetime_utils import get_next_date, get_current_date
from common_tools.decorators import exc_time
from dao.basic.stock_basic_dao import stock_basic_dao
from dao.basic.stock_dao import stock_dao
from dao.data_source import dataSource
from dao.k_data import fill_market
from dao.k_data.k_data_dao import k_data_dao
from domain.stock_pool import Stock_Pool
import pandas as pd

from feature_utils.custome_features import cal_mavol7
from feature_utils.momentum_indicators import cal_macd
from log.quant_logging import logger


class StockPoolDao:
    @exc_time
    def get_list(self):
        sql = ("select DISTINCT code, name from stock_pool")

        df = pd.read_sql(sql=sql
                         , con=dataSource.mysql_quant_conn)

        return df

    @exc_time
    def truncate(self):
        sql = "truncate table stock_pool"

        dataSource.mysql_quant_conn.execute(sql)

    @exc_time
    def query_all(self):
        with dataSource.session_ctx() as session:
            stock_dbs = session.query(Stock_Pool).all()

            return copy.deepcopy(stock_dbs)

    @exc_time
    def init_pool(self):

        self.truncate()

        stocks = stock_dao.query_all()

        k_data_list = k_data_dao.get_multiple_k_data(start=get_next_date(-720), end=get_current_date())
        df = pd.DataFrame(columns=['code', 'name'])

        for stock in stocks:
            try:

                k_data = k_data_list.loc[k_data_list['code'] == fill_market(stock.code)]
                k_data = k_data.join(cal_macd(k_data))
                k_data['turnover7'] = cal_mavol7(k_data, column='turnover')

                k_turnover7 = k_data['turnover7'].values[-1]


                if len(k_data['code'].values) == 0:
                    continue

                stock_basic = stock_basic_dao.get_by_code(stock.code)
                eps_value = stock_basic['eps'].values[0]
                profits_yoy_value = stock_basic['profits_yoy'].values[0]

                if eps_value < 0:
                    continue

                if profits_yoy_value < 0:
                    continue

                if k_turnover7 < 65000000:
                    continue

                dict = {"code": stock.code, "name": stock.name}
                df = df.append(dict, ignore_index=True)
                logger.debug("append code:%s" % stock.code)
            except Exception as e:
                logger.debug("code:%s, error:%s" % (stock.code, traceback.format_exc()))

        df.to_sql('stock_pool', dataSource.mysql_quant_engine, if_exists='append', index=False)
        '''
            df_zz = ts.get_zz500s()
            df_zz['type'] = 'zz500'
            df_hs300 = ts.get_hs300s()
            df_hs300['type'] = 'hs300'
    
            df_zz.to_sql('stock_pool', dataSource.mysql_quant_engine, if_exists='append', index=False)
            df_hs300.to_sql('stock_pool', dataSource.mysql_quant_engine, if_exists='append', index=False)
        '''



stock_pool_dao = StockPoolDao()
