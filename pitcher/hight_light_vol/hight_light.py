# ae_h - 2018/7/31
from dao.basic.stock_industry_dao import stock_industry_dao
from dao.k_data.k_data_dao import k_data_dao
from common_tools.datetime_utils import get_next_date, get_current_date
from feature_utils.custome_features import cal_mavol3
import pandas as pd
from log.quant_logging import logger

'''

bk_vol_frame = pd.Dataframe(columns=['bkcode', vol])

temp_dict = {}
bk_vol3 = 0
for bk in bks:
    for stock in bk:
        get stock k-data
            cal stock mavol3
            bk_vol3 += stock mavol3
    temp_dict['bk'] = bkcode

'''


def cal_bk_vol():
    bk_vol_frame = pd.DataFrame(columns=['bkcode', 'bk_name', 'total_mavol_3'])

    filter_list = ['BK0743', 'BK0804', 'BK0568', 'BK0707', 'BK0701', 'BK0611', 'BK0705', 'BK0612', 'BK0500']
    org_bk_code_list = list(stock_industry_dao.get_bkcode_list().values)

    bk_code_list = [c for c in org_bk_code_list if c not in filter_list]

    for bk in bk_code_list:
        bk_stocks = stock_industry_dao.get_by_bkcode(bk[0])
        bk_vol3 = 0
        try:
            bk_name = bk_stocks['bk_name'][0]
        except:
            bk_name = 'N/A'

        for code in bk_stocks['code'].values:

            stock_df = k_data_dao.get_k_data(code=code, start=get_next_date(-30), end=get_current_date())

            if len(stock_df) == 0:
                continue

            stock_df['mavol3'] = cal_mavol3(stock_df)
            try:
                bk_vol3 += stock_df['mavol3'].values[-1:][0]
            except Exception as e:
                logger.debug("code:%s, error:%s" % (code, repr(e)))
        bk_vol_frame.loc[bk_vol_frame.shape[0] + 1] = {'bkcode': bk, 'bk_name': bk_name, 'total_mavol_3': bk_vol3}

    bk_vol_frame = bk_vol_frame.sort_values('total_mavol_3', ascending=False)

    bk_vol_frame.to_csv('bk_csv.csv', encoding='utf_8_sig')


if __name__ == '__main__':
    cal_bk_vol()
