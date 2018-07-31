from sqlalchemy import Column
from sqlalchemy import DateTime, func
from sqlalchemy.ext.declarative import declarative_base, declared_attr
import datetime
import time

from sqlalchemy.orm import class_mapper


def datetime_to_timestamp(date):
    if isinstance(date, datetime.date):
        return int(time.mktime(date.timetuple()))
    else:
        return None


class BaseModel(object):

    create_time = Column(DateTime, default=func.now())
    update_time = Column(DateTime, default=func.now(), onupdate=func.now())

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    @classmethod
    def get_id(cls):
        pass

    def to_dict(self):
        columns = [c.key for c in class_mapper(self.__class__).columns]

        return dict((c, getattr(self, c)) for c in columns)

        '''
        intersection = set(self.__table__.columns.keys()) & set(self.FIELDS)
        return dict(map(
            lambda key:
            (key,
             (lambda value: self.FIELDS[key](value) if value else None)
             (getattr(self, key))),
            intersection))
        '''



Base = declarative_base(cls=BaseModel)
