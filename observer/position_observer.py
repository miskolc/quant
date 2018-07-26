from config import default_config
from dao.k_data import fill_market
from dao.trade.position_dao import position_dao

import futuquant as ft


def f(position, code):
    return position.code == code

if __name__ == '__main__':

    try:
        positions = position_dao.get_position_list()

        codes = [fill_market(p.code) for p in positions]

        futu_quote_ctx = ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST,
                                             port=default_config.FUTU_OPEND_PORT)

        state, df = futu_quote_ctx.get_market_snapshot(codes)
        # 更新实时数据
        for index, row in df.iterrows():
            code = row['code'][3:]
            last_price = row['last_price']

            position = [position for position in positions if position.code == code][0]
            position.price = last_price

            profit = round((last_price/position.price_in - 1) * 100, 2)
            print(profit)

            position_dao.update(position)
    finally:
        futu_quote_ctx.close()