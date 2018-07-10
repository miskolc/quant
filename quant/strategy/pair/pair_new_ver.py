# ae_h - 2018/7/10

import os
import sys

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_DIR)))
sys.path.append(ROOT_DIR)

import pandas as pd
import numpy as np
from quant.dao.k_data.k_data_dao import k_data_dao
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from quant.common_tools.decorators import exc_time
from quant.dao.basic.stock_industry_dao import stock_industry_dao
from quant.common_tools.datetime_utils import get_next_date


@exc_time
def code_muning_850():
    code_list = stock_industry_dao.get_stock_code_list().values.tolist()
    pair_set = set()
    for i in range(0, len(code_list)):
        for j in range(1, len(code_list)):
            code1 = code_list[i][0]
            code2 = code_list[j][0]
            code_tuple = sorted((code1, code2))
            pair_set.add((code_tuple[0], code_tuple[1]))
    return pair_set


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
    pair_set = code_muning_850()
    # pair_set = set()
    # pair_set.add(('000538', '600518'))
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
                    print(fit_result.summary)
                    coef_value = fit_result.fittedvalues
                    stationary_value = y - coef_value * x
                    mean_value = np.mean(y - coef_value * x)
                    z_score = cal_z_score(stationary_value)
                    img_path = CURRENT_DIR + '/' + code1 + '-' + code2 + '.png'

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

                    #sub1
                    plt.subplot(221)
                    plt.title(code1 + '/plot/' + code2 + '-Fit Result')
                    plt.xlabel(code1)
                    plt.ylabel(code2)
                    plt.scatter(x, y, alpha=0.8, c=['y', 'b'], label='Prices Scatter')
                    plt.plot(x, coef_value, 'r', label='OLS')

                    plt.legend()

                    #sub2
                    plt.subplot(222)
                    plt.title('Price Curve')
                    plt.xlabel(code1)
                    plt.ylabel(code2)
                    plt.plot(close_price_1_360, label=code1)
                    plt.plot(close_price_2_360, label=code2)

                    plt.legend()

                    #sub3
                    plt.subplot(212)
                    plt.title('Z-Score(current: %.4f)' % z_score.values[0])
                    plt.xlabel('Coint-Score: %.6f' % coint_score)
                    plt.plot(z_score.values, label='Z-Score')
                    plt.hlines(mean_value, 0, 1000, label='Mean')
                    plt.hlines(1, 0, 1000, colors='r', label='upper')
                    plt.hlines(-1, 0, 1000, color='g', label='lower')

                    plt.legend()

                    plt.savefig(img_path)


        except Exception as e:
            print(repr(e))
    pair_stock_df.to_csv('1.csv')


if __name__ == '__main__':
    cal_pair_stock()





    #
    # stock1 = k_data_dao.get_k_data(code='601998', start='2015-01-01', end='2017-12-31')
    # stock2 = k_data_dao.get_k_data(code='601818', start='2015-01-01', end='2017-12-31')
    #
    # stock1_price = stock1['close']
    # stock2_price = stock2['close']
    #
    # close_vect = pd.concat([stock1_price, stock2_price], axis=1)
    # close_vect.columns = ['601998', '601818']
    # close_vect = close_vect.fillna(method='ffill')
    #
    # coint_result = sm.tsa.stattools.coint(close_vect['601998'], close_vect['601818'])

    # print(coint_result[1])

    # x = close_vect['601998']
    # y = close_vect['601818']
    #
    # X = sm.add_constant(x)
    # fit_result = sm.OLS(y, X).fit()
    # print(fit_result.summary())
    #
    # sns.set_style('darkgrid')
    #
    # fig, ax = plt.subplots()
    # plt.title(code/fit_result.fittedvalues)
    # plt.xlabel(stock1['code'].values[0])
    # plt.ylabel(stock2['code'].values[0])
    # ax.scatter(x, y, s=10, alpha=0.8, c=['g', 'b'], label='s1')
    # ax.plot(x, fit_result.fittedvalues, 'r', label='OLS')
    #
    # ax.legend(loc='best')
    # plt.show()

    # regu_df = pd.DataFrame({'Stationary': y - fit_result.fittedvalues*x, 'Mean': np.mean(y - fit_result.fittedvalues*x)})
    #
    # plt.plot(regu_df['Stationary'], label='res')
    # plt.plot(regu_df['Mean'], label='mean')
    # plt.legend()
    # plt.show()
