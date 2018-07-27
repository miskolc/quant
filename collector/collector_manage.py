# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

import os
import sys

# Append project path to system path
from config import default_config

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(ROOT_DIR)

import collector.basic.stock_basic_collector as stock_basic_collector
import collector.k_data.k_data_collector  as k_data_collector
from apscheduler.schedulers.blocking import BlockingScheduler

import futuquant as ft
PROJECT_NAME = "quant-collector"


if __name__ == '__main__':
    futu_quote_ctx = ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST, port=default_config.FUTU_OPEND_PORT)


    scheduler = BlockingScheduler()
    scheduler.add_job(stock_basic_collector.collect_stock_basic, 'cron', day_of_week='1-5', hour=15, minute=30)

    scheduler.add_job(k_data_collector.collect_all_daily, 'cron', day_of_week='1-5', hour=16, minute=30, args=[futu_quote_ctx])
    scheduler.start()

