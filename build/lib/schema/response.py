from .schema import Schema
from .model import Model


class ResponseBody(Schema):

    def __init__(self, *args, content_type=None, description=None, http_code=None, model=None, **kwargs):
        if callable(model):
            model = model()
        kwargs['content_type'] = content_type
        kwargs['description'] = description
        kwargs['model'] = model
        kwargs['http_code'] = http_code
        super().__init__(*args, **kwargs)
        self.content_type = content_type
        self.description = description
        self.http_code = http_code
        self.model = model

    def dump(self) -> dict:
        results = []
        for child in self._children:
            results.append(child.dump())
        if self.model and isinstance(self.model, Model):
            model = {"$ref": "#/components/schemas/%s" % self.model.__class__.__name__}
        else:
            model = self.model.dump() if hasattr(self, 'model') and hasattr(self.model, 'dump') else None
        return {
            self.content_type: {
                "http_code": self.http_code,
                "content_type": self.content_type,
                "description": self.description,
                "schema": model,
            }
        }


class EmptyResponseBody(ResponseBody):

    def __init__(self, *args, description=None, http_code=None, model=None, **kwargs):
        kwargs['description'] = description
        kwargs['model'] = model
        kwargs['http_code'] = http_code
        content_type = None
        super().__init__(*args, content_type=content_type, **kwargs)


class JsonResponseBody(ResponseBody):

    def __init__(self, *args, description=None, http_code=None, model=None, **kwargs):
        kwargs['description'] = description
        kwargs['model'] = model
        kwargs['http_code'] = http_code
        content_type = 'application/json'
        super().__init__(*args, content_type=content_type, **kwargs)


class XmlResponseBody(ResponseBody):

    def __init__(self, *args, description=None, http_code=None, model=None, **kwargs):
        kwargs['description'] = description
        kwargs['model'] = model
        kwargs['http_code'] = http_code
        content_type = 'application/xml'
        super().__init__(*args, content_type=content_type, **kwargs)


class TextResponseBody(ResponseBody):

    def __init__(self, *args, description=None, http_code=None, model=None, **kwargs):
        kwargs['description'] = description
        kwargs['model'] = model
        kwargs['http_code'] = http_code
        content_type = 'text/plain'
        super().__init__(*args, content_type=content_type, **kwargs)


