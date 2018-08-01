from common_tools.orm_serializer import JsonEncoder
import json


class BaseHandler(object):

    def to_json(self, body_dict):
        return json.dumps(body_dict, cls=JsonEncoder)

    def on_success(self, resp, data=None):

        if data is None:
            obj = {"message": "successfully"}
            resp.body = self.to_json(obj)
            return

        if isinstance([],type(data)):
            obj = [item.to_dict() for item in data]
        elif isinstance({},type(data)):
            obj = data
        else:
            obj = data.to_dict()

        resp.body = self.to_json(obj)