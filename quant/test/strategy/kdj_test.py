# ae_h - 2018/7/7
import os
import sys

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_DIR)))
sys.path.append(ROOT_DIR)
import numpy as np
from quant.dao.k_data.k_data_dao import k_data_dao
from quant.feature_utils.momentum_indicators import acc_kdj
import pandas as pd
from quant.common_tools.decorators import exc_time
import matplotlib.pyplot as plt
from scipy import optimize


@exc_time
def cal_kdj():
    df = k_data_dao.get_k_data(code='601881', start='2017-12-01', end='2018-07-09')

    k_d_j = acc_kdj(df)

    ccb_df_with_kdj = pd.concat([df, k_d_j], axis=1)

    return ccb_df_with_kdj


def f_1(x, A, B):
    return A * x + B


if __name__ == '__main__':

    ccb_df = cal_kdj()
    ccb_df = ccb_df[-120:]

    high_tick_points = []
    low_tick_points = []
    index_tick_points = []

    for i in range(0, 120, 10):
        high_result = ccb_df[ccb_df['close'] == ccb_df['close'][i:i + 10].max()]
        high_v = high_result['close'].values[0]

        low_result = ccb_df[ccb_df['close'] == ccb_df['close'][i:i + 10].min()]
        low_v = low_result['close'].values[0]

        index_v = high_result.index.values[0]

        high_tick_points.append(high_v)
        low_tick_points.append(low_v)
        index_tick_points.append(index_v)

    x = index_tick_points
    y = high_tick_points
    l = low_tick_points


    plt.scatter(x[:], y[:], 25, label='close-high')
    plt.scatter(x[:], l[:], 25, label='close-low')

    A1, B1 = optimize.curve_fit(f_1, x, y)[0]
    C1, D1 = optimize.curve_fit(f_1, x, l)[0]
    x1 = np.arange(ccb_df.index.values[-1], 0, -10)
    y1 = A1 * x1 + B1
    l1 = C1 * x1 + D1

    # resi_slope = np.gradient(x1, y1)[-1]
    # sup_slope = np.gradient(x1, l1)[-1]

    plt.plot(x1, y1, label='resistance')
    plt.plot(x1, l1, label='support slope')
    plt.plot(ccb_df['close'], label='close price')

    print('last resistance point: %.3f' % y1[-1])
    print('last support point: %.3f' % l1[-1])

    plt.legend()
    plt.show()
