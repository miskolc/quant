# coding = utf-8
# ae_h - 2018/6/2

from quant.common_tools.decorators import exc_time
from quant.dao import dataSource
from quant.dao.basic.stock_industry_dao import StockIndustryDao
from quant.dao.k_data.k_data_dao import k_data_dao
import tushare as ts
from app.test_pack.pairs.hurst import hurst
from statsmodels.tsa.stattools import adfuller
import pandas as pd


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
def cal_pair_stocks(pair_set):
    # hs_300_code = ts.get_hs300s()['code']
    df = k_data_dao.get_k_data_all()
    df = df.set_index(['date'])
    pair_stock = pd.DataFrame(
        columns=['stock1', 'stock2', 'ispaired', 'res', 'mean', 'std', 'intervalup', 'intervaldown'])

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

            if hurst_v < 0.45 and adf_score < percent_1:
                pair_stock.loc['stock1'] = code1
                pair_stock.loc['stock2'] = code2
                pair_stock.loc['res'] = res
                pair_stock.loc['mean'] = res.mean()
                pair_stock.loc['std'] = res.std()
                pair_stock.loc['intervalup'] = res.mean() + res.std()
                pair_stock.loc['intervaldown'] = res.mean() - res.std()
                pair_stock.loc['adfscore'] = adf_score
                pair_stock.loc['percent_1'] = percent_1

                pair_stock.dropna()

            else:
                pass
        except:
            pass

    pair_stock.to_sql('pair_stock', dataSource.mysql_quant_engine, if_exists='append', index=False)
