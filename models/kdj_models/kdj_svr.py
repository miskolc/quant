# ae_h - 2018/7/16
from config import default_config
from dao.k_data.k_data_dao import k_data_dao
import futuquant as ft

df = k_data_dao.get_k_data(code='000528', start='2010-01-01', end='2017-01-01', futu_quote_ctx=ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST,port=default_config.FUTU_OPEND_PORT))

print(df)
