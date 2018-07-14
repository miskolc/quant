# ae_h - 2018/7/13
import numpy as np
from dao.k_data.k_data_dao import k_data_dao


class KDJStrategy:
    def handle_data(self, context):

        k_data_df = futu_dao.kdata.get_k_data(start=context.current_date-9, end=context.current_date)

        calcu_features()


        if k[-1] > d[-1] and k[-2] < d[-2]:
            buy()


        print(context.current_date)

    def
