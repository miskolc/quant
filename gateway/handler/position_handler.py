# ae_h - 2018/7/27
import json
import os
import sys

from common_tools.orm_serializer import serielizer

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

from dao.trade.position_dao import position_dao


class PositionHandler(object):
    def on_get(self, req, resp):
        pos_result = position_dao.query_by_code('601800')
        result = serielizer(pos_result)
        resp.context['result'] = result
