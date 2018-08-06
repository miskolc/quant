from dao.trade.strategy_dao import strategy_dao
from dao.trade.target_dao import target_dao
from gateway.common.base_handler import BaseHandler
from gateway.errors import ResourceNotFoundException


class TargetHandler(BaseHandler):
    """
    Handle for endpoint: /target/{code}
    """

    def on_get(self, req, resp, code):
        tartget_result = target_dao.query_by_code('601800')
        if tartget_result is None:
            raise ResourceNotFoundException("Can not found position.")

        self.on_success(resp=resp, data=tartget_result.to_dict())


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
