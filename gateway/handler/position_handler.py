# ae_h - 2018/7/27
import json
import os
import sys

from sqlalchemy.orm.exc import NoResultFound

from common_tools.orm_serializer import serielizer
from gateway.common.base_handler import BaseHandler
from gateway.errors import ResourceNotFoundException

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

from dao.trade.position_dao import position_dao


class PositionHandler(BaseHandler):
    def on_get(self, req, resp):
        pos_result = position_dao.query_by_code('601800')
        self.on_success(resp=resp, data=pos_result)


class PositionItemHandler(BaseHandler):
    """
    Handle for endpoint: /position/{code}
    """

    def on_get(self, req, resp, code):

        pos_result = position_dao.query_by_code(code)

        if pos_result is None:
            raise ResourceNotFoundException("Can not found position.")


        self.on_success(resp=resp, data=pos_result)

