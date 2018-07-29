import futuquant as ft

from common_tools.datetime_utils import get_next_date, get_current_date
from config import default_config
from dao.basic.stock_industry_dao import stock_industry_dao
from dao.k_data import fill_market
from dao.k_data.k_data_dao import k_data_dao
from dao.k_data_weekly.k_data_weekly_dao import k_data_weekly_dao
from feature_utils.custome_features import cal_mavol7
from feature_utils.momentum_indicators import cal_macd, acc_kdj
from feature_utils.overlaps_studies import cal_ma145
from log.quant_logging import logger
import traceback

'''
    1. close>ma145
    2. trend up(?)
    3. 周k上 macd 水上金叉 或 即将金叉
     - (>-0.35 水上金叉)
    4. 日k上 macd已经金叉(-3days)
     - (>-0.45 水上金叉)
    5. weekly vol >= pre weekly vol * 1.3
    6. mavol7 >= 7500w
    7. vol amount <15亿
    8. 净资产收益率>=20%
    9. 毛利率>=20%
    10. 市盈率asc
    11. 股息率>=1 desc
    12. 每股收益大于100%(连续两年同比增长)
    13. 净资产收益 desc
'''


def cal_stock_pool():
    df_poll = stock_industry_dao.get_stock_code_list()
    code_list = list(df_poll['code'].values)
    w_data_list = k_data_weekly_dao.get_multiple_k_data(code_list, start='2013-01-01', end=get_current_date())
    k_data_list = k_data_dao.get_multiple_k_data(code_list=code_list, start=get_next_date(-720), end=get_current_date())

    #k_data_list = k_data_list.set_index('code', inplace=True)

    # k_data_list = k_data_dao.get_market_snapshot(code_list=code_list, futu_quote_ctx=futu_quote_ctx)
    matched = []
    for code in code_list:
        rs = cal_single_stock(code, k_data_list, w_data_list)
        if rs is True:
            matched.append(code)

    print("matched:%s" % matched)


def cal_single_stock(code, k_data_list, w_data_list):
    try:
        w_data = w_data_list.loc[w_data_list['code'] == fill_market(code)]
        w_data = w_data.join(cal_macd(w_data))
        # w_data = w_data.join(acc_kdj(w_data))

        k_data = k_data_list.loc[k_data_list['code'] == fill_market(code)]
        k_data = k_data.join(cal_macd(k_data))
        if len(k_data) == 0:
            return

        k_data['ma145'] = cal_ma145(k_data)
        k_data['turnover7'] = cal_mavol7(k_data, column='turnover')

        w_pre_volume = w_data['volume'].values[-2]
        w_volume = w_data['volume'].values[-1]

        w_pre_macd = w_data['macd'].values[-1]
        w_pre_diff = w_data['diff'].values[-1]
        w_pre_dea = w_data['dea'].values[-1]

        w_macd = w_data['macd'].values[-1]
        w_diff = w_data['diff'].values[-1]
        w_dea = w_data['dea'].values[-1]
        # w_k_value = w_data['k_value'].values[-1]
        # w_d_value = w_data['d_value'].values[-1]

        k_close = k_data['close'].values[-1]
        k_ma145 = k_data['ma145'].values[-1]
        k_turnover7 = k_data['turnover7'].values[-1]

        if k_close < k_ma145:
            logger.debug("code:%s, close price less than ma145" % code)
            return False

        if k_turnover7 < 75000000:
            logger.debug("code:%s, turnover less than 75000000" % code)
            return

        if round(w_volume / w_pre_volume, 1) < 1.3:
            logger.debug("code:%s, volume  less than pre_volume * 1.3" % code)
            return False

        if (w_pre_diff < w_pre_dea and w_macd > -0.35 and w_diff > w_dea) \
                or (w_pre_diff < w_pre_dea and w_macd > -0.35 and w_dea - w_diff < abs(w_dea * 0.2)):

            macd_point = k_data_dao.get_last_macd_cross_point(k_data, window_size=5)

            # 日k上 macd已经金叉(-3days)
            if macd_point is not None:
                return True

    except Exception as e:
        logger.error("code:%s" % code)
        logger.error(traceback.format_exc())

    return False

if __name__ == '__main__':

    cal_stock_pool()
    '''
    #BK0712

    code_list = ['603616']
    w_data_list = k_data_weekly_dao.get_multiple_k_data(code_list, start='2013-01-01', end=get_current_date())
    k_data_list = k_data_dao.get_multiple_k_data(code_list=code_list, start=get_next_date(-60), end=get_current_date())
    #k_data_list = k_data_list.set_index('code', inplace=True, drop=False)
    cal_single_stock('603616',w_data_list, k_data_list)
   '''
