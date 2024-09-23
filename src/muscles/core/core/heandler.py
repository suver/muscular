import traceback
from typing import Union


class BaseResponseHandler:

    def __init__(self):
        ...

    def handler(self, response: Union[str, dict, bytes, None] = None):
        traceback.print_stack()
        return Exception(str(response))


class ResponseHandler(BaseResponseHandler):

    def handler(self, response: Union[str, dict, bytes, None] = None):
        traceback.print_stack()
        return Exception(str(response))
