# ae_h - 2018/6/25
import unittest
from inspect import getmembers, isfunction
import pandas as pd
from quant.test import before_run
from quant.dao.k_data.k_data_dao import k_data_dao
from quant.feature_utils import pattern_recognition


class Pattern_test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_pattern_reconize(self):

        col_list = []
        df = k_data_dao.get_k_data(code='000826', start='2018-06-01', end='2018-06-25', cal_next_direction=False)

        pattern_list = [r for r in getmembers(pattern_recognition) if isfunction(r[1])]

        for func in pattern_list:
            if hasattr(pattern_recognition, func[0]):
                func_feature = func[1](df)
                if isinstance(func_feature, pd.core.series.Series):
                    df[func[0]] = func_feature
                    col_list.append(func[0])
                else:
                    df = df.join(func_feature)
                    col_names_list = func_feature.columns.values
                    for col in col_names_list:
                        col_list.append(col)
        df = df.dropna()
        df.to_csv('t.csv')
