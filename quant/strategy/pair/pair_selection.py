# coding = utf-8
# ae_h - 2018/6/2
import os
import sys

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

from sqlalchemy import create_engine, MetaData

from quant.config import default_config
from quant.dao import dataSource

from quant.dao.basic.stock_industry_dao import stock_industry_dao
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import tushare as ts
from app.test_pack.pairs.hurst import hurst
from quant.common_tools.decorators import exc_time
from quant.dao.k_data.k_data_dao import k_data_dao


@exc_time
def code_muning(data):
    code_list = data['code']
    pair_set = set()
    for i in range(0, len(code_list)):
        for j in range(1, len(code_list)):
            code1 = code_list[i]
            code2 = code_list[j]
            code_tuple = sorted((code1, code2))
            pair_set.add((code_tuple[0], code_tuple[1]))
    return pair_set


@exc_time
def cal_p_value(pair_set):
    df = k_data_dao.get_k_data_all()
    df = df.set_index(['date'])

    pair_stock = pd.DataFrame(columns=['stock1', 'stock2', 'p_value'])

    for item in pair_set:
        i = 1

        try:
            code1 = item[0]
            code2 = item[1]

            stock1_close = df[df['code'] == code1]['close']
            stock2_close = df[df['code'] == code2]['close']

            coint_result = sm.tsa.stattools.coint(stock1_close, stock2_close)

            p_value = coint_result[1]

            if p_value < 0.05:
                temp_dict = {'stock1': code1, 'stock2': code2, 'p_value': p_value}
                pair_stock.loc[i] = temp_dict

                i += 1
        except:
            pass
    pair_stock.dropna()
    pair_stock.to_csv('pair_result.csv')


@exc_time
def cal_pair_stocks(pair_set):
    df = k_data_dao.get_k_data_all()
    df = df.set_index(['date'])
    pair_stock = pd.DataFrame(
        columns=['stock1', 'stock2', 'res', 'mean', 'std', 'intervalTop', 'intervalBottom', 'adfscore', 'percent_1'])
    i = 1
    for item in pair_set:

        try:
            code1 = item[0]
            code2 = item[1]

            close1 = df[df['code'] == code1]['close']
            close2 = df[df['code'] == code2]['close']

            res = close1 / close2
            hurst_v = hurst(res)
            adf_result = list(adfuller(res))
            adf_score = adf_result[0]
            percent_1 = adf_result[4]['1%']
            # sm_pvalue = sm.tsa.stattools.coint(close1, close2)

            if hurst_v < 0.45 and adf_score < percent_1:
                if industry_filter(code1, code2):
                    bk1, bk2 = industry_filter(code1, code2)
                    mean_v = res.mean()
                    std_v = res.std()
                    intervalTop = mean_v + std_v
                    intervalBottom = mean_v - std_v
                    temp_dict = {}

                    temp_dict['stock1'] = code1+bk1
                    temp_dict['stock2'] = code2+bk2
                    temp_dict['res'] = res[-1]
                    temp_dict['mean'] = mean_v
                    temp_dict['std'] = std_v
                    temp_dict['intervalTop'] = intervalTop
                    temp_dict['intervalBottom'] = intervalBottom
                    temp_dict['adfscore'] = adf_score
                    temp_dict['percent_1'] = percent_1

                    pair_stock.loc[i] = temp_dict
                    i += 1
        except:
            pass
    pair_stock.to_csv('pair_result.csv')


def fill_zero(code):
    code = str(code)
    code = code.zfill(6)
    return code


def industry_filter(code1, code2):
    industry_df = stock_industry_dao.get_list()

    bk1 = industry_df[industry_df['code'] == code1]['bk_name'].values[0]
    bk2 = industry_df[industry_df['code'] == code2]['bk_name'].values[0]

    if bk1 == bk2:
        return bk1, bk2
    else:
        return False


# pair_stock.to_sql('pair_stock', dataSource.mysql_quant_engine, if_exists='append', index=False)

if __name__ == '__main__':
    data = ts.get_hs300s()
    code_set = code_muning(data)
    cal_pair_stocks(code_set)
