from ...src.muscles.core.schema import Model
from ...src.muscles.core.schema import Column
from ...src.muscles.core.schema import Key
from ...src.muscles.core.schema import Swagger
from ...src.muscles.core.schema import QueryParameter
from ...src.muscles.core.schema import Enum
from ...src.muscles.core.schema import String
from ...src.muscles.core.schema import ApiKeyAuthSecurity
from ...src.muscles.core.schema import JsonResponseBody
from ...src.muscles.core.schema import XmlResponseBody
from ...src.muscles.core.schema import TextRequestBody


def test_Swagger():
    """
    Проверяем схему Swagger
    :return:
    """

    class SchTest(Model):
        id = Column(Key)

    r = Swagger(
        title="Test",
        name="Test 2",
        version="1.2",
        description="Test Swagger Api",
        termsOfService="https://terms",
        servers=[{"url": "/api/v1"}],
        contact_email="admin@mail.ru",
        request=TextRequestBody(description='Form', model=String, is_list=True),
        parameters=QueryParameter('query2', Enum(enum=['one', 'two']), required=False, description='Query2'),
        security=[
            ApiKeyAuthSecurity()
        ],
        response=JsonResponseBody(description='OK', model=SchTest)
    )
    assert r.dump() == {
        'info': {
            'title': 'Test',
            'version': '1.2'
        },
        'openapi': '3.0.3',
        'description': 'Test Swagger Api',
        'termsOfService': 'https://terms',
        'servers': [{'url': '/api/v1'}],
        'contact': {'email': 'admin@mail.ru'},
        'request': {
            'text/plain': {
                'description': 'Form',
                'schema': {
                    'type': 'array',
                    'items': {
                        'class': 'String',
                        'children': [],
                        'data_type': 'string',
                        'type': 'string',
                        'pattern': None,
                        'length': 255
                    }
                }
            }
        },
        'response': {
            'application/json': {
                'http_code': None,
                'content_type': 'application/json',
                'description': 'OK',
                'schema': {
                    '$ref': '#/components/schemas/SchTest'
                }
            }
        },
        'parameters': {
            'required': False,
            'explode': False,
            'description': 'Query2',
            'name': 'query2',
            'schema': {
                'class': 'Enum',
                'children': [],
                'data_type': 'enum',
                'type': 'string',
                'pattern': None,
                'enum': ['one', 'two']
            },
            'in': 'query'
        },
        'components': {
            'securitySchemes': {
                'ApiKey': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'X-Api-Token'
                }
            }
        }
    }


def test_Swagger_2():
    """
    Проверяем схему Swagger
    :return:
    """

    class SchTest(Model):
        id = Column(Key)

    r = Swagger(
        title="Test",
        name="Test 2",
        version="1.2",
        description="Test Swagger Api",
        termsOfService="https://terms",
        servers=[{"url": "/api/v1"}],
        contact_email="admin@mail.ru",
        request=[
            TextRequestBody(description='Form', model=String, is_list=True),
        ],
        parameters=[
            QueryParameter('query2', Enum(enum=['one', 'two']), required=False, description='Query2'),
        ],
        security=[
            ApiKeyAuthSecurity()
        ],
        response={
            200: [
                JsonResponseBody(description='OK', model=SchTest),
                XmlResponseBody(description='OK', model=SchTest),
            ],
            404: JsonResponseBody(description='NOT FOUND', model=SchTest),
        }
    )
    assert r.dump() == {
        'info': {
            'title': 'Test',
            'version': '1.2'
        },
        'openapi': '3.0.3',
        'description': 'Test Swagger Api',
        'termsOfService': 'https://terms',
        'servers': [{'url': '/api/v1'}],
        'contact': {'email': 'admin@mail.ru'},
        'request': [
            {
                'text/plain': {
                    'description': 'Form',
                    'schema': {
                        'type': 'array',
                        'items': {
                            'class': 'String',
                            'children': [],
                            'data_type': 'string',
                            'type': 'string',
                            'pattern': None,
                            'length': 255
                        }
                    }
                }
            }
        ],
        'response': {
            200: [
                {
                    'application/json': {
                        'http_code': None,
                        'content_type': 'application/json',
                        'description': 'OK',
                        'schema': {'$ref': '#/components/schemas/SchTest'}
                    }
                },
                {
                    'application/xml': {
                        'http_code': None,
                        'content_type': 'application/xml',
                        'description': 'OK',
                        'schema': {'$ref': '#/components/schemas/SchTest'}
                    }
                }
            ],
            404: {
                'application/json': {
                    'http_code': None,
                    'content_type': 'application/json',
                    'description': 'NOT FOUND',
                    'schema': {
                        '$ref': '#/components/schemas/SchTest'
                    }
                }
            }
        },
        'parameters': [
            {
                'required': False,
                'explode': False,
                'description': 'Query2',
                'name': 'query2',
                'schema': {
                    'class': 'Enum',
                    'children': [],
                    'data_type': 'enum',
                    'type': 'string',
                    'pattern': None,
                    'enum': ['one', 'two']
                },
                'in': 'query'
            }
        ],
        'components': {
            'securitySchemes': {
                'ApiKey': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'X-Api-Token'
                }
            }
        }
    }


