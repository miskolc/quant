# ae_h - 2018/7/27
import os
import sys

from domain.position import Position
from gateway.common.base_handler import BaseHandler
from gateway.errors import ResourceNotFoundException

from dao.trade.position_dao import position_dao

from cerberus import Validator

FIELDS = {
    "code": {
        'type': 'string',
        'required': True,
        'minlength': 6,
        'maxlength': 32
    },
}

class PositionHandler(BaseHandler):
    def on_get(self, req, resp):
        pos_result = position_dao.query_by_code('601800')
        self.on_success(resp=resp, data=pos_result)


class Collection(BaseHandler):
    def on_post(self, req, res):
        position_req = req.context['data']
        if position_req:
            position = Position()
            position.code = position_req["code"]
            position.name = position_req["name"]
            position.price = position_req["price"]
            position.price_in = position_req["price_in"]
            position.shares = position_req["shares"]
            position.strategy_code = position_req["strategy_code"]
            position_dao.update(position)



class PositionItemHandler(BaseHandler):
    """
    Handle for endpoint: /position/{code}
    """

    def on_get(self, req, resp, code):
        pos_result = position_dao.query_by_code(code)

        if pos_result is None:
            raise ResourceNotFoundException("Can not found position.")

        self.on_success(resp=resp, data=pos_result)


class PositionSearchHandler(BaseHandler):
    """
    Handle for endpoint: /position/{code}
    """

    def on_post(self, req, resp):
        search_req = req.context['data']

        rs = position_dao.query_by_strategy_code(search_req['strategy_code'])

        if rs is None:
            raise ResourceNotFoundException("Can not found position list.")

        self.on_success(resp=resp, data=rs)