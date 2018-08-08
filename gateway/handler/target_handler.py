from datetime import datetime

import falcon
from cerberus import Validator

from dao.futu_opend import futu_opend
from dao.k_data import fill_market
from dao.trade.strategy_dao import strategy_dao
from dao.trade.target_dao import target_dao
from domain.target import Target
from gateway.common.base_handler import BaseHandler
from gateway.errors import ResourceNotFoundException, InvalidRequestException

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
        'maxlength': 32
    },
    "price": {
        'type': 'float',
        'required': False,
        'min': 0
    },
    "pointcut": {
        'type': 'float',
        'required': False,
        'nullable': True,
        'min': 0
    }
}


def validate_target_create(req, res, resource, params):
    schema = {
        'code': FIELDS['code'],
        'name': FIELDS['name'],
        'strategy_code': FIELDS['strategy_code'],
        'pointcut': FIELDS['pointcut']
    }

    v = Validator(schema)

    if not v.validate(req.context['data']):
        raise InvalidRequestException(v.errors)


def validate_target_update(req, res, resource, params):
    schema = {
        'id': FIELDS['id'],
        'pointcut': FIELDS['pointcut'],
    }

    v = Validator(schema)

    if not v.validate(req.context['data']):
        raise InvalidRequestException(v.errors)


class TargetDeleteHandler(BaseHandler):
    def on_put(self, req, resp):
        id_list_req = req.context['data']

        id_list = []
        if 'id_list' in id_list_req:
            id_list = id_list_req["id_list"]

        if len(id_list) == 0:
            raise InvalidRequestException("id list can't be null")

        for id in id_list:
            target_result = target_dao.query_by_id(id)
            if target_result is None:
                raise ResourceNotFoundException("Can not found target.")

            target_dao.delete(target_result)

        self.on_success(resp)


class TargetHandler(BaseHandler):
    """
    Handle for endpoint: /target/{id}
    """

    def on_get(self, req, resp, id):
        target_result = target_dao.query_by_id(id)
        if target_result is None:
            raise ResourceNotFoundException("Can not found target.")

        self.on_success(resp=resp, data=target_result.to_dict())


class TargetSearchHandler(BaseHandler):
    """
    Handle for endpoint: /position/search
    """

    def on_post(self, req, resp):

        target_dbs = target_dao.query_all()

        if target_dbs is None:
            raise ResourceNotFoundException("Can not found position list.")

        strategy_dbs = strategy_dao.query_all()

        group = {"list": []}
        for strategy in strategy_dbs:
            target_list = [t.to_dict() for t in target_dbs if t.strategy_code == strategy.code]

            if len(target_list) > 0:
                group_item = {"strategy_code": strategy.code, "strategy_name": strategy.name,
                              "target_list": target_list}

                group["list"].append(group_item)

        self.on_success(resp=resp, data=group)


class Collection(BaseHandler):
    @falcon.before(validate_target_create)
    def on_post(self, req, res):
        target_req = req.context['data']
        if target_req:
            target = Target()
            target.code = target_req["code"]
            target.strategy_code = target_req["strategy_code"]
            target.name = target_req["name"]
            target.pointcut = target_req["pointcut"]

            target_est = target_dao.query_by_code(strategy_code=target.strategy_code, code=target.code)
            if target_est is not None:
                raise InvalidRequestException("stock has already exists")

            # 订阅
            futu_opend.subscribe(fill_market(target_req["code"]))
            state, data = futu_opend.quote_ctx.get_stock_quote(code_list=[fill_market(target_req["code"])])
            target.price = data['last_price'].values[0]
            target_dao.add(target)

        else:
            raise InvalidRequestException(target_req)

        self.on_success(res, None)

    @falcon.before(validate_target_update)
    def on_put(self, req, res):
        target_req = req.context['data']

        target = target_dao.query_by_id(id=target_req["id"])

        if target is None:
            raise ResourceNotFoundException("Can not found target.")

        if 'pointcut' in target_req:
            target.pointcut = target_req["pointcut"]

        if 'price' in target_req:
            target.price = target_req["price"]

        code = fill_market(target.code)
        futu_opend.subscribe(code)
        state, data = futu_opend.quote_ctx.get_stock_quote(code_list=[code])
        target.price = data['last_price'].values[0]

        target.update_time = datetime.now()
        target_dao.update(target)

        self.on_success(res, None)
