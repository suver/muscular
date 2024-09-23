from ...src.muscles.core.schema import Model
from ...src.muscles.core.schema import Column
from ...src.muscles.core.schema import Key
from ...src.muscles.core.schema import BasicAuthSecurity
from ...src.muscles.core.schema import ApiKeyAuthSecurity
from ...src.muscles.core.schema import BearerAuthSecurity


def test_BasicAuthSecurity():
    """
    Проверяем схему BasicAuthSecurity
    :return:
    """
    r = BasicAuthSecurity()
    assert r.dump() == {'Basic': {'type': 'http', 'scheme': 'basic'}}


def test_ApiKeyAuthSecurity():
    """
    Проверяем схему ApiKeyAuthSecurity
    :return:
    """
    r = ApiKeyAuthSecurity()
    assert r.dump() == {
        'ApiKey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-Api-Token'
        }
    }


def test_BearerAuthSecurity():
    """
    Проверяем схему BearerAuthSecurity
    :return:
    """
    r = BearerAuthSecurity()
    assert r.dump() == {
        'Bearer': {
            'type': 'http',
            'scheme': 'basic'
        }
    }


