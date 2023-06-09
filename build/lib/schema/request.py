from .schema import Schema
from .model import BaseModel
from .collection import Collection


class RequestBody(Schema):

    def __init__(self, *args, content_type=None, description=None, model=None, **kwargs):
        if callable(model):
            model = model()
        kwargs["content_type"] = content_type
        kwargs["description"] = description
        kwargs["model"] = model
        super().__init__(*args, **kwargs)
        self.content_type = content_type
        self.description = description
        self.model = model

    def dump(self) -> dict:
        results = []
        for child in self._children:
            results.append(child.dump())
        if self.model and isinstance(self.model, BaseModel):
            model = {"$ref": "#/components/schemas/%s" % self.model.__class__.__name__}
        elif self.model and isinstance(self.model, Collection):
            model = {"$ref": "#/components/schemas/%s" % self.model.__class__.__name__}
        else:
            model = self.model.dump() if hasattr(self, 'model') and hasattr(self.model, 'dump') else None
        return {
            self.content_type: {
                "description": self.description,
                "schema": model,
            }
        }


class JsonRequestBody(RequestBody):

    def __init__(self, *args, description=None, model=None, **kwargs):
        kwargs["description"] = description
        kwargs["model"] = model
        kwargs["content_type"] = 'application/json'
        super().__init__(*args, **kwargs)


class XmlRequestBody(RequestBody):

    def __init__(self, *args, description=None, model=None, **kwargs):
        kwargs["description"] = description
        kwargs["model"] = model
        kwargs["content_type"] = 'application/xml'
        super().__init__(*args, **kwargs)


class FormRequestBody(RequestBody):

    def __init__(self, *args, description=None, model=None, **kwargs):
        kwargs["description"] = description
        kwargs["model"] = model
        kwargs["content_type"] = 'application/x-www-form-urlencoded'
        super().__init__(*args, **kwargs)


class MultipartRequestBody(RequestBody):

    def __init__(self, *args, description=None, model=None, **kwargs):
        kwargs["description"] = description
        kwargs["model"] = model
        kwargs["content_type"] = 'multipart/form-data'
        super().__init__(*args, **kwargs)


class FileRequestBody(RequestBody):

    def __init__(self, *args, content_type=None, description=None, model=None, **kwargs):
        kwargs["description"] = description
        kwargs["model"] = model
        kwargs["content_type"] = content_type
        super().__init__(*args, **kwargs)


class PayloadRequestBody(RequestBody):

    def __init__(self, *args, description=None, model=None, **kwargs):
        kwargs["description"] = description
        kwargs["model"] = model
        kwargs["content_type"] = 'text/plain'
        super().__init__(*args, **kwargs)


class TextRequestBody(RequestBody):

    def __init__(self, *args, description=None, model=None, **kwargs):
        kwargs["description"] = description
        kwargs["model"] = model
        kwargs["content_type"] = 'text/plain'
        super().__init__(*args, **kwargs)


