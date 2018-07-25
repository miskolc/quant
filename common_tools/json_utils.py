from datetime import date, datetime

from common_tools.datetime_utils import DATE_TIME_FORMAT


def obj_dict(obj):
    if isinstance(obj, (datetime, date)):
        return obj.strftime(DATE_TIME_FORMAT)
    return obj.__dict__