from common_tools.orm_serializer import serielizer
import json


class BaseHandler(object):
    def to_json(self, obj):
        body_dict = serielizer(obj)
        return json.dumps(body_dict)

    def on_success(self, resp, data=None):
        result = serielizer(data)
        resp.context['result'] = result
