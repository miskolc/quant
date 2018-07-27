# ae_h - 2018/7/27
from sqlalchemy.orm import class_mapper
import datetime
import json


def serielizer(model):
    columns = [c.key for c in class_mapper(model.__class__).columns]

    return json.dumps(dict((c, getattr(model, c)) for c in columns), cls=DateEncoder, ensure_ascii=False)


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)
