
class MuscularError(Exception):

    def __init__(self, status, reason=None, body=None):
        super()
        self.status = status
        self.reason = reason if reason is not None else error_code.get(status, "Internal Error")
        self.body = body


error_code = {
    200: "OK",
    403: "Access Denied",
    404: "Not Found"
}