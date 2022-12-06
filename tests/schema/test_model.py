from muscles import FormRequestBody
from ..app.instance import Muscular
from ..app.models.sch_test import SchTest
from ..app.models.user import User


column_name_User = {
    'name': {
        'class': 'String',
        'children': [],
        'data_type': 'string',
        'type': 'string',
        'format': None,
        'length': 255,
        'index': True,
        'unique': False,
        'default': None,
        'required': False,
        'title': None,
        'description': None,
        'nullable': False,
        'value': None,
        'primary_key': False,
        'example': None
    }
}

column_id_SchTest = {
    'SchTest': {
        'type': 'object',
        'properties': {
            'id': {
                'class': 'Key',
                'children': [],
                'data_type': 'key',
                'type': 'big_integer',
                'format': None,
                'index': False,
                'unique': False,
                'default': None,
                'required': False,
                'title': None,
                'description': None,
                'nullable': False,
                'value': None,
                'primary_key': False,
                'example': None
            }
        }
    }
}


def test_zero():
    """
    Проверяем работоспособность схемы
    :return:
    """
    u = SchTest(id="id")
    assert u.dump() == column_id_SchTest


def test_model():
    """
    Модели схемы
    :return:
    """
    u = User(name="test name", status="blocked")
    u.email = 'mmm@mail.ru'

    assert u.columns["name"].value == "test name"
    assert u.status == "blocked"
    assert u.columns["name"].dump() == column_name_User


def test_request():
    """
    Схемы запросов
    :return:
    """
    u = User(name="test name", status="blocked")
    u.email = 'mmm@mail.ru'

    r = FormRequestBody(model=u)
    assert r.content_type == 'application/x-www-form-urlencoded'
    assert r.model.columns["name"].dump() == column_name_User






