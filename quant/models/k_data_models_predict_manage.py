# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/19

import os
import sys

# Append project path to system path
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

from quant.log.quant_logging import logger
from quant.config import default_config
from sqlalchemy import create_engine, MetaData
from quant.dao.data_source import dataSource
from quant.models.k_data import k_data_manage
import warnings
from datetime import datetime
import tushare as ts
from quant.notification_tools.notify_pack import mail_content_render, mail_notify_sender
from quant.dao.k_data.k_data_predict_log_dao import k_data_predict_log_dao
from quant.common_tools.datetime_utils import get_current_date



def predict():
    '''
    now = datetime.now().strftime('%Y-%m-%d')
    is_holiday = ts.is_holiday(now)
    # 如果是假日, 跳过
    if is_holiday:
        return
    '''
    k_data_manage.predict_k_data()


if __name__ == '__main__':
    warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)


    predict()

    df_predict = k_data_predict_log_dao.get_predict_log_list(get_current_date())
    html = mail_content_render('mail_predict_daily_report_template.html', {'df_predict': df_predict})
    mail_notify_sender(default_config.MAIL_TO, 'Predict Daily Report', html)
