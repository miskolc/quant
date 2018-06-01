# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/1

from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'


def get_current_date():
    return datetime.now().strftime(DATE_FORMAT)
