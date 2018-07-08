# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

import os
import sys

# Append project path to system path
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

import quant.collector.k_data.k_data_collector as k_data
import quant.collector.k_data_60m.k_data_60m_collector as k_data_60m
import quant.collector.k_data_60m.index_k_data_60m_collector as index_k_data_60m
import quant.collector.k_data.k_data_technical_feature_collector as k_data_feature_collector
import quant.collector.k_data.index_k_data_collector as index_k_data
import quant.collector.k_data_60m.k_data_60m_technical_feature_collector as k_data_60m_technical_feature_collector
import schedule
import time

PROJECT_NAME = "quant-collector"

if __name__ == '__main__':

    # feature_collector.collect_hs300_full()
    # k_data_60m.collect_hs300_full()
    # index_k_data_60m.collect_index_china_daily()
    # k_data_60m_technical_feature_collector.collect_hs300_daily()


    #schedule.every().day.at("15:30").do(k_data_60m.collect_hs300_daily)
    schedule.every().day.at("15:30").do(k_data.collect_all)
    schedule.every().day.at("15:32").do(index_k_data.collect_index_china_daily)
    schedule.every().day.at("16:30").do(index_k_data.collect_index_hk_daily)
    schedule.every().day.at("8:30").do(index_k_data.collect_index_usa_daily)

    #schedule.every().day.at("15:32").do(index_k_data_60m.collect_index_china_daily)

    #schedule.every().day.at("15:35").do(k_data_feature_collector.collect_hs300_daily)
    #schedule.every().day.at("15:35").do(k_data_60m_technical_feature_collector.collect_hs300_daily)



    while True:
        schedule.run_pending()
        time.sleep(1)
