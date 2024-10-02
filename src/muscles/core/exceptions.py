
class ErrorException(Exception):

    def __init__(self, status=400, reason=None, body=None, traceback=None):
        self.status = status
        self.reason = reason
        self.body = body
        self.traceback = traceback
        super().__init__(self.reason)


class AttributeErrorException(ErrorException):

    def __init__(self, status=400, reason=None, body=None, traceback=None):
        self.status = status
        self.reason = reason
        self.body = body
        self.traceback = traceback
        super().__init__(status=self.status, reason=self.reason, body=self.body, traceback=self.traceback)


class ModelException(ErrorException):

    def __init__(self, status=400, reason=None, body=None, traceback=None):
        self.status = status
        self.reason = reason
        self.body = body
        self.traceback = traceback
        super().__init__(status=self.status, reason=self.reason, body=self.body, traceback=self.traceback)


class ApplicationException(ErrorException):

    def __init__(self, status=500, reason=None, body=None, traceback=None):
        self.status = status
        self.reason = reason
        self.body = body
        self.traceback = traceback
        super().__init__(status=self.status, reason=self.reason, body=self.body, traceback=self.traceback)


class AccessDeniedException(ErrorException):

    def __init__(self, status=403, reason="Access Denied", body=None, traceback=None):
        self.status = status
        self.reason = reason
        self.body = body
        self.traceback = traceback
        super().__init__(status=self.status, reason=self.reason, body=self.body, traceback=self.traceback)


class RequestErrorException(ErrorException):

    def __init__(self, status=403, reason=None, body=None, traceback=None):
        self.status = status
        self.reason = reason
        self.body = body
        self.traceback = traceback
        super().__init__(status=self.status, reason=self.reason, body=self.body, traceback=self.traceback)


class NotFoundException(ErrorException):
    ...


class IsExistsException(ErrorException):
    ...


class UpdateErrorException(ErrorException):
    ...


class InsertErrorException(ErrorException):
    ...


class NotAuthenticationException(ErrorException):
    ...
