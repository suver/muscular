import io
import json
from muscles import WsgiStrategy
from ..app.instance import Muscular


def start_response(status, headers):
    pass


environ = {
    'REQUEST_METHOD': 'GET',
    'REQUEST_URI': '/api/v1/test',
    'PATH_INFO': '/api/v1/test',
    'QUERY_STRING': '',
    'SERVER_PROTOCOL': 'HTTP/1.1',
    'SCRIPT_NAME': '',
    'SERVER_NAME': 'a0c8b2e9a5a7',
    'SERVER_PORT': '8080',
    'UWSGI_ROUTER': 'http',
    'REMOTE_ADDR': '172.22.0.1',
    'REMOTE_PORT': '34030',
    'HTTP_X_API_TOKEN': 'hfHfdjfr746Hfkdbd3uhHdl',
    'HTTP_USER_AGENT': 'PostmanRuntime/7.29.2',
    'HTTP_ACCEPT': '*/*',
    'HTTP_CACHE_CONTROL': 'no-cache',
    'HTTP_POSTMAN_TOKEN': '2241d11b-aeb6-4ed1-a0d3-c120168d96b6',
    'HTTP_HOST': 'localhost:8080',
    'HTTP_ACCEPT_ENCODING': 'gzip, deflate, br', 'HTTP_CONNECTION': 'keep-alive',
    'wsgi.input': io.BytesIO(),
    'wsgi.version': (1, 0),
    'wsgi.errors': io.BytesIO(),
    'wsgi.run_once': False,
    'wsgi.multithread': False,
    'wsgi.multiprocess': False,
    'wsgi.url_scheme': 'http',
    'uwsgi.version': b'2.0.20',
    'uwsgi.node': b'a0c8b2e9a5a7'
}


def test_check_get():
    """
    Проверяем работоспособность схемы
    :return:
    """
    environ.update({
        'REQUEST_METHOD': 'GET',
        'REQUEST_URI': '/api/v1/test',
        'PATH_INFO': '/api/v1/test',
        'CONTENT_TYPE': 'application/json',
    })
    muscular = Muscular()
    muscular.context.strategy = WsgiStrategy
    app = muscular(environ, start_response)
    for pr in app:
        assert pr == b'{"method": "GET", "request": {"url": "http://localhost:8080/api/v1/test"}}'


def test_check_post():
    """
    Проверяем работоспособность схемы
    :return:
    """
    environ.update({
        'REQUEST_METHOD': 'POST',
        'REQUEST_URI': '/api/v1/test',
        'PATH_INFO': '/api/v1/test',
        'CONTENT_TYPE': 'application/json',
    })
    muscular = Muscular()
    muscular.context.strategy = WsgiStrategy
    app = muscular(environ, start_response)
    for pr in app:
        pr = json.loads(pr)
        assert pr['method'] == "POST"


def test_check_delete():
    """
    Проверяем работоспособность схемы
    :return:
    """
    environ.update({
        'REQUEST_METHOD': 'DELETE',
        'REQUEST_URI': '/api/v1/test',
        'PATH_INFO': '/api/v1/test',
        'CONTENT_TYPE': 'application/json',
    })
    muscular = Muscular()
    muscular.context.strategy = WsgiStrategy
    app = muscular(environ, start_response)
    for pr in app:
        print(pr)
        assert pr == b'{"method": "DELETE"}'


def test_check_put():
    """
    Проверяем работоспособность схемы
    :return:
    """
    environ.update({
        'REQUEST_METHOD': 'PUT',
        'REQUEST_URI': '/api/v1/test',
        'PATH_INFO': '/api/v1/test',
        'CONTENT_TYPE': 'application/json',
    })
    muscular = Muscular()
    muscular.context.strategy = WsgiStrategy
    app = muscular(environ, start_response)
    for pr in app:
        print(pr)
        assert pr == b'{"method": "PUT"}'


def test_check_show():
    """
    Проверяем работоспособность схемы
    :return:
    """
    environ.update({
        'REQUEST_METHOD': 'GET',
        'REQUEST_URI': '/api/v1/test/1',
        'PATH_INFO': '/api/v1/test/1',
        'CONTENT_TYPE': 'application/json',
    })
    muscular = Muscular()
    muscular.context.strategy = WsgiStrategy
    app = muscular(environ, start_response)
    for pr in app:
        assert pr == b'{"id": "1", "method": "GET", "request": {"url": "http://localhost:8080/api/v1/test/1"}}'


def test_check_change():
    """
    Проверяем работоспособность схемы
    :return:
    """
    environ.update({
        'REQUEST_METHOD': 'POST',
        'REQUEST_URI': '/api/v1/test/1',
        'PATH_INFO': '/api/v1/test/1',
        'CONTENT_TYPE': 'application/json',
    })
    muscular = Muscular()
    muscular.context.strategy = WsgiStrategy
    app = muscular(environ, start_response)
    for pr in app:
        assert pr == b'{"id": "1", "method": "POST", "request": {"url": "http://localhost:8080/api/v1/test/1"}}'


def test_check_drop():
    """
    Проверяем работоспособность схемы
    :return:
    """
    environ.update({
        'REQUEST_METHOD': 'DELETE',
        'REQUEST_URI': '/api/v1/test/1',
        'PATH_INFO': '/api/v1/test/1',
        'CONTENT_TYPE': 'application/json',
    })
    muscular = Muscular()
    muscular.context.strategy = WsgiStrategy
    app = muscular(environ, start_response)
    for pr in app:
        assert pr == b'{"id": "1", "method": "DELETE", "request": {"url": "http://localhost:8080/api/v1/test/1"}}'

