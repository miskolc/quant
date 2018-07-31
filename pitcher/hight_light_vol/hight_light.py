# ae_h - 2018/7/31
from dao.basic.stock_industry_dao import stock_industry_dao
from dao.k_data.k_data_dao import k_data_dao
import pandas as pd

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
    bk_vol_frame = pd.DataFrame(columns=['bkcode', 'total_vol'])
    temp_dict = {}
    bk_vol3 = 0

    bk_code_list = stock_industry_dao.get_bkcode_list()
    for bk in bk_code_list['bk_code'].values:
        bk_stocks = stock_industry_dao.get_by_bkcode(bk)
        for stock in bk_stocks['code'].values:
            stock_df =




if __name__ == '__main__':
    cal_bk_vol()
