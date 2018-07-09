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
import pandas as pd

def cal_signal(code):
    data = k_data_tech_feature_dao.get_k_data(code, '2018-07-01', get_current_date())
    df_k_data = k_data_dao.get_k_data(code, start='2018-06-01', end=get_current_date())

    price = df_k_data['close'].tail(1).values[0]

    ma10 = data['ma10'].values[-1]
    if price < ma10:
        return

    if price < 4:
        return

    k_pre = data['k_value'].values[-2]
    d_pre = data['d_value'].values[-2]

    k = data['k_value'].values[-1]
    d = data['d_value'].values[-1]

    # 上穿, 金叉
    if k_pre < d_pre and abs(k - d) < 1:
        return "up"

    # 下穿, 死叉
    if k_pre > d_pre and abs(k - d) < 1:
        return "down"

    return "hold", k, d;


if __name__ == '__main__':

    df_pool = stock_pool_dao.get_list()

    data = pd.DataFrame(columns=['code', 'date', 'name', 'bk_code', 'bk_name', 'k', 'd', 'label'])

    list = []
    for index, row in df_pool.iterrows():
        code = row['code']

        try:
            label, k, d = cal_signal(code)

            if label == 'up':
                #data = df.append({'bk_code': bk_code, 'bk_name': bk_name, 'code': code, 'name': name}, ignore_index=True)

                list.append(code)
        except:
            pass
    print(list)

    data.to_sql('k_data_strategy_kdj_log', dataSource.mysql_quant_engine, if_exists='append', index=False)

    '''
    label = cal_signal(600017)

    print(label)
    '''
