# ae_h - 2018/7/27
import os
import sys

import falcon

from domain.position import Position
from gateway.common.base_handler import BaseHandler
from gateway.errors import ResourceNotFoundException, InvalidRequestException

from dao.trade.position_dao import position_dao

from cerberus import Validator

FIELDS = {
    "code": {
        'type': 'string',
        'required': True,
        'minlength': 6,
        'maxlength': 6
    },
    "name": {
        'type': 'string',
        'required': True,
        'minlength': 0,
        'maxlength': 64
    },
    "strategy_code": {
        'type': 'string',
        'required': True,
        'minlength': 6,
        'maxlength': 32
    },
    "price": {
        'type': 'float',
        'required': True,
        'min': 0
    },
    "price_in": {
        'type': 'float',
        'required': True,
        'min': 0
    },
    "shares": {
        'type': 'integer',
        'required': True,
        'min': 100
    },
}


def validate_position_create(req, res, resource, params):
    schema = {
        'code': FIELDS['code'],
        'name': FIELDS['name'],
        'strategy_code': FIELDS['strategy_code'],
        'price_in': FIELDS['price_in'],
        'shares': FIELDS['shares']
    }

    v = Validator(schema)

    if not v.validate(req.context['data']):
        raise InvalidRequestException(v.errors)

def validate_position_update(req, res, resource, params):
    schema = {
        'price_in': FIELDS['price_in'],
        'shares': FIELDS['shares']
    }

    v = Validator(schema)

    if not v.validate(req.context['data']):
        raise InvalidRequestException(v.errors)

class PositionHandler(BaseHandler):
    def on_get(self, req, resp):
        pos_result = position_dao.query_by_code('601800')
        self.on_success(resp=resp, data=pos_result)


class Collection(BaseHandler):
    @falcon.before(validate_position_create)
    def on_post(self, req, res):
        position_req = req.context['data']
        if position_req:
            position = Position()
            position.code = position_req["code"]
            position.strategy_code = position_req["strategy_code"]
            position.name = position_req["name"]
            position.price_in = position_req["price_in"]
            position.shares = position_req["shares"]

            position_dao.add(position)
        else:
            raise InvalidRequestException(position_req)

    def on_put(self, req, res):
        position_req = req.context['data']




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
