from .schema import Schema


class BaseSecurity(Schema):

    schema = {}
    securitySchema = ""

    def __init__(self, *args, key=None, securitySchema=None, securityType=None, scope=None, **kwargs):
        self.securitySchema = securitySchema
        self.schema = {
            "type": securityType,
        }
        self.scope = scope or []
        self.key = key or securitySchema
        for key, val in kwargs.items():
            self.schema.update({key: val})
        kwargs["securitySchema"] = securitySchema
        kwargs["securityType"] = securityType
        super().__init__(*args, **kwargs)

    def dump(self) -> dict:
        return {self.key: self.schema}


class BasicAuthSecurity(BaseSecurity):
    securitySchema = "BasicAuth"

    def __init__(self, *args, key='Basic', securityType='http', scheme='basic', scope=None, **kwargs):
        self.scope = scope or []
        kwargs["key"] = key
        kwargs["securitySchema"] = self.securitySchema
        kwargs["type"] = securityType
        kwargs["scheme"] = scheme
        super().__init__(*args, **kwargs)


class ApiKeyAuthSecurity(BaseSecurity):
    securitySchema = "ApiKeyAuth"

    def __init__(self, *args, key='ApiKey', securityType='apiKey', location='header', name='X-Api-Token', scope=None,
                 **kwargs):
        self.scope = scope or []
        kwargs["securitySchema"] = self.securitySchema
        kwargs["key"] = key
        kwargs["type"] = securityType
        kwargs["in"] = location
        kwargs["name"] = name
        super().__init__(*args, **kwargs)


class BearerAuthSecurity(BaseSecurity):
    securitySchema = "BearerAuth"

    def __init__(self, *args, key='Bearer', securityType='http', scheme='basic', scope=None, **kwargs):
        self.scope = scope or []
        kwargs["key"] = key
        kwargs["securitySchema"] = self.securitySchema
        kwargs["type"] = securityType
        kwargs["scheme"] = scheme
        super().__init__(*args, **kwargs)
