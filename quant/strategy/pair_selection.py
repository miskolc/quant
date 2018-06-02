# coding = utf-8
# ae_h - 2018/6/2

import tushare as ts

def cal_pair_stocks(start_from='2017-01-01'):

    code_list = list(ts.get_hs300s()['code'])

    sql = "select * from k_data where `date`> start_from"
