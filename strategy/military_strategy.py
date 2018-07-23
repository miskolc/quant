import futuquant as ft
import talib

from config import default_config
from dao.k_data import fill_market
from dao.k_data_weekly.k_data_weekly_dao import k_data_weekly_dao
from dao.basic.stock_industry_dao import stock_industry_dao
from dao.k_data.k_data_dao import k_data_dao
from feature_utils.momentum_indicators import cal_macd

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

        #k_data_list = k_data_dao.get_market_snapshot(code_list=code_list, futu_quote_ctx=futu_quote_ctx)

        for code in code_list:
            df_week = k_data_weekly_dao.get_k_data(code, start=None, end=None, futu_quote_ctx=futu_quote_ctx)

            df_week = df_week.join(cal_macd(df_week))

            code = code

            pre_volume = df_week['volume'].values[-2]
            volume = df_week['volume'].values[-1]
            macd = df_week['macd'].values[-1]

            if volume > pre_volume * 1.3 and macd > 0:
                print(code, pre_volume,volume)


            #k_data = k_data_list.loc[k_data_list['code'] == fill_market(code)]






    finally:
        futu_quote_ctx.close()