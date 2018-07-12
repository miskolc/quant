# ae_h - 2018/7/5
from dao.basic.stock_industry_dao import stock_industry_dao
import pandas as pd


def fill_zero(code):
    code = str(code)
    code = code.zfill(6)
    return code


industry_df = stock_industry_dao.get_list()

# bk_code = set(list(industry_df['bk_code'].values))
# print(bk_code)

df = pd.read_csv('/Users/yw.h/quant-awesome/quant/strategy/pair/pair_result.csv')

# print(industry_df[industry_df['code'] == '000001']['bk_code'])

list = []
for index, row in df.iterrows():
    code1 = fill_zero(str(int(row['stock1'])))
    code2 = fill_zero(str(int(row['stock2'])))

    bk1 = industry_df[industry_df['code'] == code1]['bk_name'].values[0]
    bk2 = industry_df[industry_df['code'] == code2]['bk_name'].values[0]

    if bk1 == bk2:
        list.append((code1+bk1, code2+bk2))


print(list)





