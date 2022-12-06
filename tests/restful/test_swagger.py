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


def test_check_swagger():
    """
    Проверяем работоспособность схемы
    :return:
    """
    environ.update({
        'REQUEST_METHOD': 'GET',
        'REQUEST_URI': '/swagger',
        'PATH_INFO': '/swagger',
        'CONTENT_TYPE': 'text/html',
    })
    muscular = Muscular()
    muscular.context.strategy = WsgiStrategy
    app = muscular(environ, start_response)
    for pr in app:
        assert len(pr) > 500


def test_check_schema():
    """
    Проверяем работоспособность схемы
    :return:
    """
    environ.update({
        'REQUEST_METHOD': 'GET',
        'REQUEST_URI': '/api/v1/schema',
        'PATH_INFO': '/api/v1/schema',
        'CONTENT_TYPE': 'application/json',
    })
    muscular = Muscular()
    muscular.context.strategy = WsgiStrategy
    app = muscular(environ, start_response)
    for pr in app:
        pr = json.loads(pr)
        assert pr['info']['title'] == 'Api v1'
        assert pr['info']['version'] == '1.0'
        assert pr['openapi'] == '3.0.3'
        assert pr['contact']['email'] == '**@**.info'
        assert pr['description'] == 'Системный Api'
        assert pr['termsOfService'] == 'http://swagger.io/terms/'
        assert pr['servers'] == [{'url': '/api/v1'}]
        assert pr['paths']['/test'].get('get')
        assert pr['paths']['/test'].get('post')
        assert pr['paths']['/test'].get('put')
        assert pr['paths']['/test'].get('delete')
        assert pr['paths']['/test/{id}'].get('get')
        assert pr['paths']['/test/{id}'].get('post')
        assert pr['paths']['/test/{id}'].get('delete')



