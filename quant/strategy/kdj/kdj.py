import os
import sys

# Append project path to system path
from quant.dao import dataSource

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

from quant.common_tools.datetime_utils import get_current_date
from quant.dao.basic.stock_pool_dao import stock_pool_dao
from quant.dao.k_data.k_data_dao import k_data_dao
from quant.dao.k_data.k_data_tech_feature_dao import k_data_tech_feature_dao
from quant.dao.basic.stock_industry_dao import stock_industry_dao
from quant.log.quant_logging import logger
import pandas as pd


def cal_signal(data):
    k_pre = data['k_value'].values[-2]
    d_pre = data['d_value'].values[-2]

    k = data['k_value'].values[-1]
    d = data['d_value'].values[-1]

    # 上穿, 金叉
    if k_pre < d_pre and abs(k - d) < 1:
        return "up",k,d

    # 下穿, 死叉
    if k_pre > d_pre and abs(k - d) < 1:
        return "down",k,d

    return "hold",k,d


def cal_single_stock(code):
    data = k_data_tech_feature_dao.get_k_data(code, get_current_date(), get_current_date())
    df_k_data = k_data_dao.get_k_data(code, start='2018-06-01', end=get_current_date())

    price = df_k_data['close'].tail(1).values[0]

    ma10 = data['ma10'].values[-1]
    if price < ma10:
        return None, None, None

    if price < 4:
        return None, None, None

    label, k, d = cal_signal(data)

    return label, k, d;


if __name__ == '__main__':

    df_pool = stock_pool_dao.get_list()

    data = pd.DataFrame(columns=['code', 'date', 'name', 'bk_code', 'bk_name', 'k', 'd', 'label'])

    list = []
    for index, row in df_pool.iterrows():
        code = row['code']

        try:
            label, k, d = cal_single_stock(code)

            if label is None:
                continue

            if label == 'up':
                df_stock_industry = stock_industry_dao.get_by_code(code)
                name = df_stock_industry['name'].values[0]

                if name.find('ST') > -1:
                    continue

                bk_code = df_stock_industry['bk_code'].values[0]
                bk_name = df_stock_industry['bk_name'].values[0]

                data = data.append({'bk_code': bk_code, 'bk_name': bk_name, 'code': code,
                                    'name': name, 'date': get_current_date(), 'label':label, 'k':k, 'd':d},
                                   ignore_index=True)
        except Exception as e:
            logger.debug("code:%s, error:%s" % (code, repr(e)))


    data.to_sql('k_data_strategy_kdj_log', dataSource.mysql_quant_engine, if_exists='append', index=False)

    '''
    label = cal_single_stock('600006')

    print(label)

    '''