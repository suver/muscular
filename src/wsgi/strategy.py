from ..core.strategy import Strategy
from watchdog.events import LoggingEventHandler
from .server import WsgiTransport, WsgiServer
from ..storage import StorageMapper
storageMapper = StorageMapper()

event_handler = LoggingEventHandler()


class WsgiStrategy(Strategy):
    """
    Стратегия WSGI сервера
    """

    locale = storageMapper.get('locale')
    logger = storageMapper.get('logger')

    def execute(self, *args, **kwargs):
        """
        Запрусаем обработку запросов
        :param args:
        :param kwargs:
        :return:
        """
        host = kwargs['host'] if hasattr(kwargs, 'host') else 'localhost'
        port = kwargs['port'] if hasattr(kwargs, 'port') else 8080
        self.logger.info("Запускаем обработку WSGI сервера на %s:%s", host, port, extra={
            'environ': kwargs['environ']
        })
        server = WsgiServer(host, port)
        transport = kwargs.get('transport', WsgiTransport)
        server.init_transport(transport)
        try:
            return server.execute(*args, **kwargs)
        except Exception as err:
            self.logger.exception(str(err))

