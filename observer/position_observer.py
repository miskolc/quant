
import os
import sys

# Append project path to system path
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(ROOT_DIR)


from apscheduler.schedulers.blocking import BlockingScheduler

from config import default_config
from dao.k_data import fill_market
from dao.trade.position_dao import position_dao
from datetime import datetime
import futuquant as ft


def monitor():
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

            profit = round((last_price / position.price_in - 1) * 100, 2)
            position.profit = profit
            position.update_time = datetime.now()
            position_dao.update(position)
    finally:
        futu_quote_ctx.close()

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(monitor, 'cron', day_of_week='1-5', hour='9-15',second='*/15')
    scheduler.start()