# ae_h - 2018/7/7
import os
import sys

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)
import numpy as np
from quant.dao.k_data.k_data_dao import k_data_dao
from quant.feature_utils.momentum_indicators import acc_kdj
import pandas as pd
from quant.common_tools.decorators import exc_time

@exc_time
def cal_kdj():

    df = k_data_dao.get_k_data_all()

    k_d_j = acc_kdj(df)

    df_with_kdj = pd.concat([df, k_d_j], axis=1)

    print(df_with_kdj)


