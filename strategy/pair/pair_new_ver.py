# ae_h - 2018/7/10

import os
import sys

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_DIR)))
sys.path.append(ROOT_DIR)

import pandas as pd
import numpy as np
from dao.k_data.k_data_dao import k_data_dao
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from common_tools.decorators import exc_time
from dao.basic.stock_industry_dao import stock_industry_dao
from dao.basic.stock_pool_dao import stock_pool_dao


# @exc_time
# def code_muning_850():
#     code_list = stock_industry_dao.get_stock_code_list().values.tolist()
#     pair_set = set()
#     for i in range(0, len(code_list)):
#         for j in range(1, len(code_list)):
#             code1 = code_list[i][0]
#             code2 = code_list[j][0]
#             code_tuple = sorted((code1, code2))
#             pair_set.add((code_tuple[0], code_tuple[1]))
#     # return pair_set
#     print(len(pair_set))
#     print(pair_set)


@exc_time
def code_muning():
    code_list = stock_pool_dao.get_list().values.tolist()
    # code_list = ['a', 'b', 'c', 'd', 'e']
    lenth = len(code_list) - 1
    pair_sets = []

    for i in range(0, lenth, 1):
        for j in range(lenth, 0, -1):
            if i == j or j < i:
                continue
            code1 = code_list[i][0]
            code2 = code_list[j][0]
            pair_sets.append((code1, code2))

    # print(pair_sets)
    # print(len(pair_sets))
    return pair_sets

@exc_time
def industry_filter(code1, code2):
    industry_df = stock_industry_dao.get_list()

    bk1 = industry_df[industry_df['code'] == code1]['bk_name'].values[0]
    bk2 = industry_df[industry_df['code'] == code2]['bk_name'].values[0]

    if bk1 == bk2:
        return bk1
    else:
        return False


@exc_time
def cal_z_score(series):
    return (series - series.mean()) / np.std(series)


@exc_time
def cal_pair_stock():
    pair_set = code_muning()
    # pair_set = set()
    # pair_set.add(('002500', '002736'))
    whole_df = k_data_dao.get_k_data_all()

    pair_stock_df = pd.DataFrame(
        columns=['stock1', 'stock2', 'bk', 'coint_score', 'stationary', 'mean', 'z_score', 'img_path'])

    sns.set_style('darkgrid')
    i = 1

    for code_pair in pair_set:

        try:
            code1 = code_pair[0]
            code2 = code_pair[1]

            close_price_1_360 = whole_df[whole_df['code'] == code1]['close'][-360:]
            close_price_2_360 = whole_df[whole_df['code'] == code2]['close'][-360:]

            close_vect = pd.concat([close_price_1_360, close_price_2_360], axis=1)

            close_vect.columns = [code1, code2]
            close_vect = close_vect.fillna(method='ffill')
            close_vect = close_vect.dropna()

            coint_result = sm.tsa.stattools.coint(close_vect[code1], close_vect[code2])
            coint_score = coint_result[1]

            if coint_score < 0.05:
                if industry_filter(code1, code2):
                    x = close_vect[code1]
                    y = close_vect[code2]

                    X = sm.add_constant(x)

                    fit_result = sm.OLS(y, X).fit()
                    f_value = fit_result.fittedvalues
                    coef_value = fit_result.params[1]
                    stationary_value = y - coef_value * x
                    # mean_value = np.mean(y - coef_value * x)
                    z_score = cal_z_score(stationary_value)
                    mean_value = np.mean(z_score)
                    img_path = CURRENT_DIR + '/plot/' + code1 + '-' + code2 + '.png'

                    temp_dict = {}
                    temp_dict['stock1'] = code1
                    temp_dict['stock2'] = code2
                    temp_dict['bk'] = industry_filter(code1, code2)
                    temp_dict['coint_score'] = coint_score
                    temp_dict['stationary'] = stationary_value.values[0]
                    temp_dict['mean'] = mean_value
                    temp_dict['z_score'] = z_score.values[0]
                    temp_dict['img_path'] = img_path

                    pair_stock_df.loc[i] = temp_dict

                    plt.figure(12, figsize=(20, 10))

                    # sub1
                    plt.subplot(221)
                    plt.title(code1 + '-' + code2 + '-Fit Result')
                    plt.xlabel(code1)
                    plt.ylabel(code2)
                    plt.scatter(x, y, alpha=0.8, c=['y', 'b'], label='Prices Scatter')
                    plt.plot(x, f_value, 'r', label='OLS')

                    plt.legend()

                    # sub2
                    plt.subplot(222)
                    plt.title('Price Curve')
                    plt.xlabel(code1)
                    plt.ylabel(code2)
                    plt.plot(close_price_1_360, label=code1)
                    plt.plot(close_price_2_360, label=code2)

                    plt.legend()

                    # sub3
                    plt.subplot(212)
                    plt.title('Z-Score(current: %.4f)' % z_score.values[-1])
                    plt.xlabel('Coint-Score: %.6f' % coint_score)
                    plt.plot(z_score.values, color='b', label='Z-Score')
                    plt.axhline(mean_value, label='Mean')
                    plt.axhline(1.0, label='upper', linestyle='--', c='r')
                    plt.axhline(-1.0, label='lower', linestyle='--', c='g')

                    plt.legend()

                    plt.savefig(img_path)
                    plt.close()


        except Exception as e:
            print(repr(e))
    pair_stock_df.to_csv('pair_new.csv')


if __name__ == '__main__':
    code_muning()
