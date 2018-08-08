# ae_h - 2018/7/27
import os
import sys

import falcon

from dao.trade.strategy_dao import strategy_dao
from domain.position import Position
from gateway.common.base_handler import BaseHandler
from gateway.errors import ResourceNotFoundException, InvalidRequestException
from dao.trade.position_dao import position_dao
from cerberus import Validator
from datetime import datetime

FIELDS = {
    "id": {
        'type': 'integer',
        'required': True
    },
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
        'required': False,
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
        'id': FIELDS['id'],
        'code': FIELDS['code'],
        'name': FIELDS['name'],
        'strategy_code': FIELDS['strategy_code'],
        'price_in': FIELDS['price_in'],
        'price': FIELDS['price_in'],
        'shares': FIELDS['shares']
    }

    v = Validator(schema)

    if not v.validate(req.context['data']):
        raise InvalidRequestException(v.errors)



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

        self.on_success(res, None)

    @falcon.before(validate_position_update)
    def on_put(self, req, res):
        position_req = req.context['data']
        position = position_dao.query_by_id(position_req["id"])

        if position is None:
            raise ResourceNotFoundException("Can not found position.")

        position.price_in = position_req["price_in"]
        position.price = position_req["price"]
        position.shares = position_req["shares"]
        position.update_time = datetime.now()
        position_dao.update(position)

        self.on_success(res, None)

class PositionHandler(BaseHandler):
    """
    Handle for endpoint: /position/{id}
    """

    def on_get(self, req, resp,id):
        pos_result = position_dao.query_by_id(id)

        if pos_result is None:
            raise ResourceNotFoundException("Can not found position.")

        self.on_success(resp=resp, data=pos_result.to_dict())


    def on_delete(self, req, resp, id):
        pos_result = position_dao.query_by_id(id)
        if pos_result is None:
            raise ResourceNotFoundException("Can not found target.")

            position_dao.delete(pos_result)

        self.on_success(resp)


class PositionSearchHandler(BaseHandler):
    """
    Handle for endpoint: /position/search
    """

    def on_post(self, req, resp):

        position_dbs = position_dao.query_all()

        if position_dbs is None:
            raise ResourceNotFoundException("Can not found position list.")

        strategy_dbs = strategy_dao.query_all()
        group = {"list": []}
        for strategy in strategy_dbs:
            position_list = [t.to_dict() for t in position_dbs if t.strategy_code == strategy.code]
            if len(position_list) > 0:
                group_item = {"strategy_code": strategy.code, "strategy_name": strategy.name,
                              "position_list": position_list}

                group["list"].append(group_item)

        self.on_success(resp=resp, data=group)
