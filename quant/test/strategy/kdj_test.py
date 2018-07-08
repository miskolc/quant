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
import seaborn as sns
import matplotlib.pyplot as plt


@exc_time
def cal_kdj():
    df = k_data_dao.get_k_data(code='601939', start='2017-12-01', end='2018-07-06')

    k_d_j = acc_kdj(df)

    ccb_df_with_kdj = pd.concat([df, k_d_j], axis=1)

    return ccb_df_with_kdj


if __name__ == '__main__':
    ccb_df = cal_kdj()

    print(ccb_df['k'])

    # ccb_k_gradient = np.gradient(ccb_df['k'].rolling(center=False, window=2).mean())

    # corr = ccb_df['k'].rolling(center=False, window=2).var()

    values = ccb_df['k'].values
    gradient_arr = np.gradient(values)

    sns.set(style="darkgrid")
    plt.plot(ccb_df['k'], label='k')
    plt.plot(ccb_df['d'], label='d')
    plt.plot(gradient_arr, label='gradient')
    plt.legend()
    plt.show()