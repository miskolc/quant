import falcon
from cerberus import Validator

from dao.trade.strategy_dao import strategy_dao
from dao.trade.target_dao import target_dao
from domain.target import Target
from gateway.common.base_handler import BaseHandler
from gateway.errors import ResourceNotFoundException, InvalidRequestException
from datetime import datetime
from collections import namedtuple

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
        'required': False,
        'min': 0
    },
    "pointcut": {
        'type': 'float',
        'required': False,
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
        'code': FIELDS['code'],
        'name': FIELDS['name'],
        'strategy_code': FIELDS['strategy_code'],
        'price': FIELDS['price'],
        'pointcut': FIELDS['pointcut'],
    }

    v = Validator(schema)

    if not v.validate(req.context['data']):
        raise InvalidRequestException(v.errors)



class TargetHandler(BaseHandler):
    """
    Handle for endpoint: /target/{code}
    """

    def on_get(self, req, resp, code):
        target_result = target_dao.query_by_code('601800')
        if target_result is None:
            raise ResourceNotFoundException("Can not found position.")

        self.on_success(resp=resp, data=target_result.to_dict())


class TargetSearchHandler(BaseHandler):
    """
    Handle for endpoint: /position/search
    """

    def on_post(self, req, resp):
        #search_req = req.context['data']

        target_dbs = target_dao.query_all()

        if target_dbs is None:
            raise ResourceNotFoundException("Can not found position list.")

        strategy_dbs = strategy_dao.query_all()

        group = {"list":[]}
        for strategy in strategy_dbs:
            target_list = [t.to_dict() for t in target_dbs if t.strategy_code == strategy.code]

            if len(target_list) >0 :
                group_item = {"strategy_code": strategy.code, "strategy_name": strategy.name,"target_list": target_list}

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

            target_dao.add(target)
        else:
            raise InvalidRequestException(target_req)

        self.on_success(res, None)

    @falcon.before(validate_target_update)
    def on_put(self, req, res):
        target_req = req.context['data']

        target = target_dao.query_by_code(strategy_code=target_req["strategy_code"], code=target_req["code"])

        if target is None:
            raise ResourceNotFoundException("Can not found target.")

        if 'pointcut' in target_req:
            target.pointcut = target_req["pointcut"]

        if 'price' in target_req:
            target.price = target_req["price"]

        target.update_time = datetime.now()
        target_dao.update(target)

        self.on_success(res, None)