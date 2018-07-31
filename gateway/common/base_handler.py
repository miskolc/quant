from common_tools.orm_serializer import JsonEncoder
import json


class BaseHandler(object):


    def on_success(self, resp, data=None):
        #result = serielizer(data)
        obj = {"data": data}

        resp.body = json.dumps(obj, cls=JsonEncoder)