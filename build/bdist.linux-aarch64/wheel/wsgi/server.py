import cgitb
import json
import os
import io
import urllib
from urllib.parse import unquote
from .request import Request, RequestMaker
from .response import Response
from .routers import routes, itinerary
from ..core.errors import MuscularError
import cgi
from urllib.parse import unquote
from ..storage import StorageMapper
storageMapper = StorageMapper()

MAX_LINE = 64 * 1024
MAX_HEADERS = 100
TIMEOUT = 2
MAX_CONNECTIONS = 1000


class Transport:
    """
    Транспорт протокола стратегии
    """

    locale = storageMapper.get('locale')
    logger = storageMapper.get('logger')

    server = None

    def __init__(self):
        pass

    def init_server(self, server):
        self.server = server

    def make_response(self, response):
        pass

    def make_request(self):
        pass


class WsgiTransport(Transport):
    """
    Транспорт стратегии WSGI
    """

    locale = storageMapper.get('locale')
    logger = storageMapper.get('logger')

    def execute(self, *args, **kwargs):
        """
        Исполняем условия транспорта
        :param args:
        :param kwargs[environ]: Окружение запроса
        :param kwargs[start_response]: Метод для ответа
        :return:
        """
        self.environ = kwargs['environ']
        self.start_response = kwargs['start_response']
        return self.handler(self.environ, self.start_response)

    def handler(self, environ, start_response):
        """
        Обработчик транспорта

        :param environ: Переменные окружения запроса
        :param start_response: Метод ответа
        :return:
        """
        request = self.make_request(environ)
        if request is None:
            self.logger.debug(self.locale('HTTP Ответ 400 от сервера "Bad request"'))
            raise MuscularError(400, 'Bad request', 'Malformed request line')
        return self.server.handler(request)

    def make_response(self, response):
        """
        Отправляем ответ
        :param response: объект ответа
        :return:
        """
        self.send_header(str(response.http_status), response.headers)
        yield response.body

    def send_header(self, http_status, headers):
        """
        Передаем заголовки ответа
        :param http_status: HTTP статус ответа
        :param headers: Заголовки
        :return:
        """
        return self.start_response(str(http_status), headers)

    def make_request(self, environ):
        """
        Формируем обхект запроса на основании переменных запроса
        :param environ: Переменные запроса
        :return: Request
        """
        requestMaker = RequestMaker(environ)
        request = requestMaker.make()

        self.logger.debug(self.locale('Формируем тело Request'), extra={
            'request': request.__dict__
        })
        return request


#
# class TCPSocketTransport(HttpTransport):
#     __charset = 'iso-8859-1'
#
#     def execute(self, *args, **kwargs):
#         '''
#         :param args[0]: host
#         :param args[1]: port
#         :param kwargs:
#         :return:
#         '''
#         self.host = args[0]
#         self.port = args[1]
#         server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
#         # server.setblocking(0)
#         server.settimeout(TIMEOUT)
#         all_threads = []
#         try:
#             server.bind((self.host, self.port))
#             server.listen(MAX_CONNECTIONS)
#             while True:
#                 try:
#                     connect, _ = server.accept()
#                     t = threading.Thread(target=self.handler, args=(connect,))
#                     t.start()
#
#                     all_threads.append(t)
#                 except ConnectionResetError:
#                     connect = None
#                 except Exception as e:
#                     # self.send_error(connect, e)
#                     traceback.print_exc(file=sys.stdout)
#         finally:
#             if server:
#                 server.close()
#             for t in all_threads:
#                 t.join()
#         return
#
#     def handler(self, connect):
#         try:
#             self.reader = connect.makefile('rb')
#             self.writer = connect.makefile('wb')
#             request = self.make_request()
#             if request is None:
#                 raise MuscularError(400, 'Bad request', 'Malformed request line')
#             self.server.handler(request)
#         except ConnectionResetError:
#             connect = None
#         except Exception as e:
#             # self.send_error(connect, e)
#             traceback.print_exc(file=sys.stdout)
#         if connect:
#             connect.close()
#
#     def make_response(self, response):
#         try:
#             status_line = f'HTTP/1.1 {response.status} {response.reason}\r\n'
#             self.writer.write(status_line.encode('iso-8859-1'))
#
#             if response.headers:
#                 for (key, value) in response.headers:
#                     header_line = f'{key}: {value}\r\n'
#                     self.writer.write(header_line.encode('iso-8859-1'))
#
#             self.writer.write(b'\r\n')
#
#             if response.body:
#                 self.writer.write(response.body)
#
#             if hasattr(self.writer, 'flush'):
#                 self.writer.flush()
#             if self.writer:
#                 self.writer.close()
#         except Exception as err:
#             print('Internal Error:', err)
#             traceback.print_exc(file=sys.stdout)
#         return
#
#     def make_request(self):
#         headers = []
#         size = 0
#         while True:
#             line = self.reader.readline()
#             if len(line) > MAX_LINE:
#                 raise MuscularError(494, 'Request header too large')
#             if b'Content-Length' in line:
#                 s = re.sub("[\r\n]", "", line)
#                 h = s.split(':')
#                 size = h[1]
#             if line in (b'\r\n', b'\n', b''):
#                 break
#             headers.append(line)
#
#         if len(headers[1:]) > MAX_HEADERS:
#             raise MuscularError(494, 'Too many headers')
#         headers = Parser().parsestr(b''.join(headers[1:]).decode(self.__charset))
#
#         words = headers[0].decode(self.__charset).split()
#         if len(words) != 3:
#             raise HTTPErrorMuscularError(400, 'Bad request', 'Malformed request line')
#         method, target, protocol = words
#         if protocol != 'HTTP/1.1':
#             raise HTTPErrorMuscularError(505, 'HTTP Version Not Supported')
#
#         host = self.headers.get('Host')
#         if not host:
#             raise MuscularError(400, 'Bad request', 'Host header is missing')
#
#         if not size:
#             body = b''
#         else:
#             body = self.reader.read(size)
#
#         request = Request(
#             method=method,
#             protocol=protocol,
#             url=target,
#             server=(self.host, self.port),
#             remote_addr=None,
#             headers=headers,
#             body=body,
#         )
#         if self.reader and hasattr(self.reader, 'close'):
#             self.reader.close()
#         return request


class WsgiServer:
    """
    Объект сервера WSGI
    """

    __transport_class = WsgiTransport
    __transport = WsgiTransport
    __host = 'localhost'
    __port = 80

    locale = storageMapper.get('locale')
    logger = storageMapper.get('logger')

    def __init__(self, host, port):
        self.__host = host
        self.__port = port

        self.__transport = self.__transport_class()
        self.__transport.init_server(self)

    def init_transport(self, transport):
        """
        Инициализируем транспорт
        :param transport: Транспорт
        :return:
        """
        self.__transport_class = transport
        self.__transport = transport()
        self.__transport.init_server(self)

    def execute(self, *args, **kwargs):
        """
        Метод исполнения протокола сервера
        :param args:
        :param kwargs:
        :return:
        """
        try:
            return self.__transport.execute(*args, **kwargs)
        except Exception as e:
            return self.send_error(e)

    def handler(self, request):
        """
        Обработчик сервера
        :param request: Запрос к серверу
        :return:
        """
        self.logger.debug(self.locale('Получаем Request(%s)', request), extra={
            'request': request.__dict__
        })

        headers = []
        for header in request.headers:
            headers.append('%s: %s' % (header, request.headers[header]))
        self.logger.info(self.locale("{protocol} {method} {url}",
                                     method=request.method,
                                     url=request.url,
                                     protocol=request.protocol,
                                     ), extra={
            'request': request.__dict__,
            'method': request.method,
            'url': request.url,
            'protocol': request.protocol,
        })
        self.logger.debug(self.locale("{protocol} {method} {url}\t\n {headers}\t\n {body}",
                                      method=request.method,
                                      url=request.url,
                                      protocol=request.protocol,
                                      headers="\n".join(headers),
                                      body=request.body
                                      ), extra={
            'request': request.__dict__,
            'method': request.method,
            'url': request.url,
            'protocol': request.protocol,
            'headers': "\n".join(headers),
            'body': request.body
        })

        static = routes.get_current_static(request)
        if static:
            return self.handle_static(static, request)
        else:
            return self.handle_request(request)

    def handle_request(self, request):
        """
        Обработчик запроса к серверу
        :param request: Объект запроса
        :return:
        """
        for key, instance in itinerary.instance_list():
            call, dictionary = instance.get_current_route(request)
            if call:
                request.route = call
                request.itinerary = instance
                break

        if request.route:
            if request.route['redirect'] and request.route['redirect'] is not None:
                resp = Response.redirect(request.route['redirect'])
            else:
                try:
                    if hasattr(request.route['handler'], 'controller'):
                        resp = request.route['handler'](request.route['handler'].controller(),
                                                        request=request,
                                                        **dictionary)
                    else:
                        resp = request.route['handler'](request=request, **dictionary)
                except MuscularError as me:
                    raise MuscularError(me.status, me.reason, me.body)

                if not isinstance(resp, Response) and isinstance(resp, str):
                    resp = Response.body(200, body=resp)
                elif not isinstance(resp, Response) and isinstance(resp, bytes):
                    resp = Response.body(200, body=resp)
                elif not isinstance(resp, Response) and isinstance(resp, dict):
                    resp = Response.body(200, body=resp)
                elif not isinstance(resp, Response) and isinstance(resp, tuple):
                    kwargs = {}
                    status = 200
                    if len(resp) >= 0:
                        kwargs['body'] = resp[0]
                    if len(resp) >= 1:
                        status = resp[1]
                    if len(resp) >= 2:
                        kwargs['headers'] = resp[2]
                    resp = Response.body(status, **kwargs)
                elif not isinstance(resp, Response):
                    resp = Response.body(200, body=resp)

                if hasattr(request.itinerary, 'modify_response'):
                    resp = request.itinerary.modify_response(resp)

                headers = []
                for header in resp.headers:
                    headers.append('%s: %s' % (header[0], header[1]))
                self.logger.debug(self.locale("Ответ {http_status}\n {headers}\n {body}",
                                              resp=resp,
                                              headers="\n".join(headers),
                                              http_status=resp.http_status,
                                              body=resp.body,
                                              ))
            return self.__transport.make_response(resp)
        self.logger.debug(self.locale("Не удалось найти подходящий роутер в системе"))
        raise MuscularError(404, 'Not found')

    def handle_static(self, static, request):
        """
        Обработчик статических файлов
        :param static: Путь к диреткории с файлами
        :param request: Объект запроса
        :return:
        """
        path = request.path.replace(static['prefix'] + '/', '', 1)
        resp_file = os.path.join(static['directory'], unquote(path))

        if not os.path.isfile(resp_file):
            self.logger.debug(self.locale("Не удалось найти подходящий файл"))
        try:
            resp = Response.file(200, file=resp_file)

            if static['handler'] is not None:
                resp = static['handler'](resp)

            headers = []
            for header in resp.headers:
                headers.append('%s: %s' % (header[0], header[1]))
            self.logger.debug(self.locale("Ответ STATIC {http_status}\n {headers}\n {body}",
                                          resp=resp,
                                          headers="\n".join(headers),
                                          http_status=resp.http_status,
                                          body=resp.body,
                                          ))

            self.__transport.send_header(resp.status, resp.headers)
            with io.open(resp_file, "rb") as f:
                yield f.read()
        except Exception as e:
            self.logger.exception(self.locale("Обработка статического файла закончилась ошибкой"))
            raise MuscularError(404, 'Not found')

    def send_error(self, err):
        """
        Отправляет ответ ошибки
        :param err: Объект ошибки или текст ошибки
        :return:
        """
        try:
            status = err.status if hasattr(err, 'status') else 500
            reason = err.reason if hasattr(err, 'reason') else str(err)
            body = err.body if hasattr(err, 'body') else str(err)
        except Exception as e:
            status = 500
            reason = b'Internal Server Error'
            body = b'Internal Server Error'

        print('Internal Error:', err)
        self.logger.exception(str(err))
        # traceback.print_exc(file=sys.stdout)

        resp = Response.error(status, reason=reason, body=body)
        # call = routes.get_current_error_handler(resp)

        for key, instance in itinerary.instance_list():
            call = instance.get_current_error_handler(resp)
            if call:
                break

        if call is not None:
            resp = call['handler'](resp)
            if not isinstance(resp, Response) and isinstance(resp, str):
                resp = Response.error(status, reason=reason, body=resp)
            elif not isinstance(resp, Response) and isinstance(resp, bytes):
                resp = Response.error(status, reason=reason, body=resp)
            elif not isinstance(resp, Response) and isinstance(resp, dict):
                resp = Response.error(status, reason=reason, body=resp)
            elif not isinstance(resp, Response) and isinstance(resp, tuple):
                kwargs = {}
                if len(resp) >= 0:
                    kwargs['reason'] = resp[0]
                if len(resp) >= 1:
                    status = resp[1]
                if len(resp) >= 2:
                    kwargs['headers'] = resp[2]
                resp = Response.error(status, **kwargs)
            elif not isinstance(resp, Response):
                resp = Response.error(status, reason=reason, body=resp)

            headers = []
            for header in resp.headers:
                headers.append('%s: %s' % (header[0], header[1]))
            self.logger.debug(self.locale("Ответ ERROR {http_status}\n {headers}\n {body}",
                                          resp=resp,
                                          headers="\n".join(headers),
                                          http_status=resp.http_status,
                                          body=resp.body,
                                          ))
        return self.__transport.make_response(resp)

