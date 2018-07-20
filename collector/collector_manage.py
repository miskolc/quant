# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

import os
import sys

# Append project path to system path
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(ROOT_DIR)

import collector.basic.stock_basic_collector as stock_basic_collector

import schedule
import time

PROJECT_NAME = "quant-collector"

if __name__ == '__main__':

    #k_data_feature_collector.collect_full_daily()
    #k_data.collect_all_daily();
    #index_k_data.collect_index_china_daily();
    #k_data_feature_collector.collect_full_daily()

    #schedule.every().day.at("15:30").do(k_data.collect_all_daily)
    #schedule.every().day.at("15:32").do(index_k_data.collect_index_china_daily)
    #schedule.every().day.at("16:30").do(index_k_data.collect_index_hk_daily)
    #schedule.every().day.at("8:30").do(index_k_data.collect_index_usa_daily)
    #schedule.every().day.at("15:35").do(k_data_feature_collector.collect_full_daily)

    #schedule.every().friday.at("15:35").do(k_data_week_collector.collect_all_weekly)

    #schedule.every().day.at("15:32").do(index_k_data_60m.collect_index_china_daily)

    #
    schedule.every().day.at("15:35").do(stock_basic_collector.collect_stock_basic)



    while True:
        schedule.run_pending()
        time.sleep(1)
