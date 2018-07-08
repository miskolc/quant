# ae_h - 2018/7/7
import os
import sys

import datetime

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
import matplotlib as mpl


@exc_time
def cal_kdj():
    df = k_data_dao.get_k_data(code='600547', start='2017-12-01', end='2018-07-06')

    k_d_j = acc_kdj(df)

    ccb_df_with_kdj = pd.concat([df, k_d_j], axis=1)

    return ccb_df_with_kdj


if __name__ == '__main__':
    ccb_df = cal_kdj()

    for i in range(10, 120, 10):
        price = ccb_df['close'].rolling(window=i).max()
