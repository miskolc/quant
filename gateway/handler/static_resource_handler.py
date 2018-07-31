import mimetypes

import falcon


class StaticResourceHandler(object):
    def on_get(self, req, resp, filename):
        # do some sanity check on the filename
        resp.status = falcon.HTTP_200

        path = 'static/' + filename
        filetype = mimetypes.guess_type(path, strict=True)[0]
        resp.content_type = filetype

        with open(path, 'r') as f:
            resp.body = f.read()
