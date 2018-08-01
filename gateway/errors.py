import falcon

RESOURCE_NOT_FOUND_EXCEPTION = {
    'status': falcon.HTTP_404,
    'code': 404,
    'title': 'Resource not found'
}

ERR_UNKNOWN = {
    'status': falcon.HTTP_500,
    'code': 500,
    'title': 'Unknown Error'
}

INVALID_REQUEST_EXCEPTION = {
    'status': falcon.HTTP_400,
    'code': 400,
    'title': 'Invalid Request'
}

class AppError(Exception):
    def __init__(self, error=ERR_UNKNOWN, description=None):
        self.error = error
        self.error['description'] = description

    @property
    def code(self):
        return self.error['code']

    @property
    def title(self):
        return self.error['title']

    @property
    def status(self):
        return self.error['status']

    @property
    def description(self):
        return self.error['description']

    @staticmethod
    def handle(exception, req, res, error=None):
        res.status = exception.status
        error = {'code': exception.code, 'message': exception.title}
        if exception.description:
            error['description'] = exception.description
        res.body = falcon.json.dumps({'error': error})


class ResourceNotFoundException(AppError):
    def __init__(self, description=None):
        super().__init__(RESOURCE_NOT_FOUND_EXCEPTION)
        self.error['description'] = description


class InvalidRequestException(AppError):
    def __init__(self, description=None):
        super().__init__(INVALID_REQUEST_EXCEPTION)
        self.error['description'] = description