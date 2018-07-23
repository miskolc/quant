import futuquant as ft

from common_tools.datetime_utils import get_next_date
from config import default_config
from dao.basic.stock_industry_dao import stock_industry_dao
from dao.k_data import fill_market
from dao.k_data.k_data_dao import k_data_dao
from dao.k_data_weekly.k_data_weekly_dao import k_data_weekly_dao
from feature_utils.custome_features import cal_mavol7
from feature_utils.momentum_indicators import cal_macd,acc_kdj
from feature_utils.overlaps_studies import cal_ma145
from log.quant_logging import logger
import traceback
'''
- 军工:BK0490

   close>ma145
  趋势向上
   周k macd红
   周k kdj接近金叉
   周vol >= 周vol-1x1.3
   mavol7 > 7500w
   vol amount < 15亿
'''


if __name__ == '__main__':
    futu_quote_ctx = ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST,
                                              port=default_config.FUTU_OPEND_PORT)

    try:

        df_industry = stock_industry_dao.get_by_bkcode('BK0490')
        code_list = list(df_industry['code'].values)
        #code_list = ['600196','601398']
        w_data_dict = k_data_weekly_dao.get_multiple_history_kline(code_list=code_list, start='2013-01-01', end=get_next_date(-5), futu_quote_ctx=futu_quote_ctx)
        k_data_dict = k_data_dao.get_multiple_history_kline(code_list=code_list, start=None, end=None, futu_quote_ctx=futu_quote_ctx)


        rs = []
        for code in code_list:

            try:
                w_data = w_data_dict[fill_market(code)]
                w_data = w_data.join(cal_macd(w_data))
                w_data = w_data.join(acc_kdj(w_data))

                k_data = k_data_dict[fill_market(code)]
                k_data['ma145'] = cal_ma145(k_data)
                k_data['turnover7'] = cal_mavol7(k_data, column='turnover')

                w_pre_volume = w_data['volume'].values[-2]
                w_volume = w_data['volume'].values[-1]
                w_macd = w_data['macd'].values[-1]
                w_diff = w_data['diff'].values[-1]
                w_dea = w_data['dea'].values[-1]
                w_k_value = w_data['k_value'].values[-1]
                w_d_value = w_data['d_value'].values[-1]

                k_close = k_data['close'].values[-1]
                k_ma145 = k_data['ma145'].values[-1]
                k_turnover7 = k_data['turnover7'].values[-1]

                if k_close > k_ma145 \
                        and k_turnover7 > 75000000 \
                        and round(w_volume/w_pre_volume, 1) >= 1.3 \
                        and (w_macd > 0 or w_diff > w_dea)\
                        and (w_k_value < w_d_value or abs(w_d_value-w_d_value) < 10):
                    rs.append(code)
            except Exception as e:
                logger.error("code:%s" % code)
                logger.error(traceback.format_exc())

        print("rs:%s" % rs)


    finally:
        futu_quote_ctx.close()