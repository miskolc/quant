import sys
import unittest

from common_tools.datetime_utils import get_current_date
from dao.k_data.k_data_predict_log_dao import k_data_predict_log_dao
from test import before_run

from notification_tools import mail_content_render, mail_notify_sender
from config import default_config


class Notify_Pack_Test(unittest.TestCase):
    def setUp(self):
        before_run()
        print(default_config.TEMPLATE_DIR)
        sys.path.append(default_config.TEMPLATE_DIR)

    def test_mail_content_render(self):
        df_predict = k_data_predict_log_dao.get_predict_log_list(get_current_date())

        html = mail_content_render('mail_predict_daily_report_template.html', { 'df_predict': df_predict})

        print(html)

    def test_mail_notify_sender(self):
        df_predict = k_data_predict_log_dao.get_predict_log_list(get_current_date())
        html = mail_content_render('mail_predict_daily_report_template.html', {'df_predict': df_predict})
        mail_notify_sender(default_config.MAIL_TO, 'Predict Daily Report', html)
        #greg.ch@fowtech.com

