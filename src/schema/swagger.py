from .schema import Schema


class Swagger(Schema):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = {'info': {}, 'openapi': '3.0.3'}
        if kwargs.get('title'):
            self.schema['info']['title'] = kwargs['title']
        elif kwargs.get('name'):
            self.schema['info']['title'] = kwargs.get('name')
        if kwargs.get('version'):
            self.schema['info']['version'] = kwargs.get('version')
        if kwargs.get('description'):
            self.schema['description'] = kwargs.get('description')
        if kwargs.get('termsOfService'):
            self.schema['termsOfService'] = kwargs.get('termsOfService')
        if kwargs.get('servers') and isinstance(kwargs.get('servers'), list):
            self.schema['servers'] = kwargs.get('servers')
        if kwargs.get('contact_email'):
            self.schema['contact'] = {}
            self.schema['contact']['email'] = kwargs.get('contact_email')

        if kwargs.get('request'):
            self.request = kwargs.get('request')
        if kwargs.get('response'):
            self.response = kwargs.get('response')
        if kwargs.get('parameters'):
            self.parameters = kwargs.get('parameters')


    def dump(self) -> dict:
        results = []
        for child in self._children:
            results.append(child.dump())
        if hasattr(self, "request") and self.request is not None:
            self.schema['request'] = self.request.dump()
        if hasattr(self, "response") and self.response is not None:
            self.schema['response'] = self.response.dump()
        if hasattr(self, "parameters") and self.parameters is not None:
            self.schema['parameters'] = self.parameters.dump()
        return self.schema
