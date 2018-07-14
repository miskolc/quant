# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

import os
import sys

# Append project path to system path
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

from models.k_data import k_data_manage
import warnings
from datetime import datetime
from dao.basic.trade_date_dao import trade_date_dao


def training(start, end):

    now = datetime.now().strftime('%Y-%m-%d')
    is_holiday = trade_date_dao.is_holiday(now)
    # 如果是假日, 跳过
    if is_holiday:
        return

    k_data_manage.training_k_data(start, end)



if __name__ == '__main__':
    warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

    training(int(sys.argv[1]),int(sys.argv[2]))
    #schedule.every().day.at("14:40").do(predict)
    #schedule.every().day.at("17:00").do(training)

    #while True:
        #schedule.run_pending()
        #time.sleep(1)
