# ae_h - 2018/7/5

import os
import sys
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

import pandas as pd
from quant.dao.k_data.k_data_dao import k_data_dao

whole_df = k_data_dao.get_k_data_all()

df = whole_df.drop_duplicates(['code'], inplace=True)


