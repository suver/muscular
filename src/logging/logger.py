import logging
import traceback
from logging.config import dictConfig
from ..configuration import Configurator

# ---------------------------------------------------------------------------
#   Level related stuff
# ---------------------------------------------------------------------------
#
# Default levels and level names, these can be replaced with any positive set
# of values having corresponding names. There is a pseudo-level, NOTSET, which
# is only really there as a lower limit for user-defined levels. Handlers and
# loggers are initialized with NOTSET so that they will log all messages, even
# at user-defined levels.
#

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


class ColorFilter(logging.Filter):
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    LIGHT = '\033[97m'
    DARK = '\033[90m'
    RED = '\033[91m'

    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    COLOR = {
        "NOTSET": GREEN,
        "DEBUG": DARK,
        "INFO": CYAN,
        "WARNING": BLUE,
        "WARN": BLUE,
        "ERROR": YELLOW,
        "FATAL": RED,
        "CRITICAL": RED,
    }

    def filter(self, record):
        record.msg = "{start}{message}{end}".format(
            start=ColorFilter.COLOR[record.levelname],
            message=record.msg,
            end=self.ENDC
        )
        return True


class SecretFilter(logging.Filter):
    """
    Filter для скрытия некоторой информации

    logger:
      version: 1
      filters:les.src.logging.ColorFilter
      secret:
        (): muscles.src.logging.SecretFilter
        patterns: [ 'poper' ]
    """

    def __init__(self, patterns):
        super(SecretFilter, self).__init__()
        self._patterns = patterns

    def filter(self, record):
        record.msg = self.redact(record.msg)
        if isinstance(record.args, dict):
            for k in record.args.keys():
                record.args[k] = self.redact(record.args[k])
        else:
            record.args = tuple(self.redact(arg) for arg in record.args)
        return True

    def redact(self, msg):
        msg = isinstance(msg, str) and msg or str(msg)
        for pattern in self._patterns:
            msg = msg.replace(pattern, "***")
        return msg


class SecretFormatter(object):
    """
    Formatter для скрытия некоторой информации
    logger:
      version: 1
      formatters:
        secret:
          (): muscles.src.logging.SecretFormatter
          format: "%(message)s %(filename)s:%(lineno)d"
          datefmt: "%H:%M:%S"
          patterns: [ 'popper' ]
    """

    def __init__(self, patterns=None, fmt=None, datefmt=None, style='%', validate=True):
        self.formatter = logging.Formatter(fmt=fmt, datefmt=datefmt, style=style, validate=validate)
        self._patterns = patterns

    def format(self, record):
        msg = self.formatter.format(record)
        for pattern in self._patterns:
            msg = msg.replace(pattern, "***")
        return msg

    def __getattr__(self, attr):
        return getattr(self.formatter, attr)


class Logger(object):
    """
    Класс логирования

    config = Configurator(file=config_file)
    logger = Logger('default', config=config.get('logger'), exc_info=False)

    ВНИМАНИЕ: Объект должен быть установлен и сконфигурирован одним из первых, что бы логирование полностью
    охватывало события в системе

    """
    _instances = {}

    def __call__(cls, name, *args, **kwargs):
        """
        Данная реализация не учитывает возможное изменение передаваемых
        аргументов в `__init__`.

        :param name:
        :param args:
        :param kwargs:
        :return:
        """
        key = '//'.join([str(cls), str(name)])
        if key not in cls._instances:
            instance = super().__call__(name, *args, **kwargs)
            cls._instances[key] = instance
        return cls._instances[key]

    def __init__(self, name,
                 config: Configurator = None,
                 level: [CRITICAL | FATAL | ERROR | WARNING | WARN | INFO | DEBUG | NOTSET] = None,
                 exc_info: bool = False):
        """
        Конструктор логирования

        :param name: домен по умолчанию
        :param config: Объект класса Configurator. По умолчанию None
        :param level: Уровень логирования. Один из CRITICAL|FATAL|ERROR|WARNING|WARN|INFO|DEBUG|NOTSET
        :param exc_info: Если Истина то будет так же добавлена отладочная информация
        """
        self.logger = logging.getLogger(name)
        self.exc_info = exc_info
        if level is not None:
            self.logger.setLevel(level)
        if config is not None:
            dictConfig(config.value())

    def log(self,
            level: [CRITICAL | FATAL | ERROR | WARNING | WARN | INFO | DEBUG | NOTSET],
            msg: str, *args,
            exc_info: bool = None,
            extra: dict = {},
            stack_info: bool = False,
            stacklevel: int = 3,
            **kwargs
            ):
        """
        Заносит информацию в лог

        :param level: Уровень логирования. Один из CRITICAL|FATAL|ERROR|WARNING|WARN|INFO|DEBUG|NOTSET
        :param msg: сообщение
        :param args: Дополнительные аргументы, которые будут использованы в сообщении
        :param exc_info: Если Истина то будет так же добавлена отладочная информация
        :param extra: Заносит дополнительную информацию, которую можно использовать в сообщение в дополнении к оладке
        :param stack_info: Если Истина добавляет стек
        :param stacklevel: С какого уровня брать стек
        :return:
        """
        if exc_info is None:
            exc_info = self.exc_info
        return self.logger.log(level, msg, *args, stacklevel=stacklevel,
                               exc_info=exc_info, extra=extra, stack_info=stack_info)

    def debug(self, msg, *args, **kwargs):
        """
        Добавляет сообщение уровня DEBUG

        :param msg: сообщение
        :param args: Дополнительные аргументы, которые будут использованы в сообщении
        :param exc_info: Если Истина то будет так же добавлена отладочная информация
        :param extra: Заносит дополнительную информацию, которую можно использовать в сообщение в дополнении к оладке
        :param stack_info: Если Истина добавляет стек
        :param stacklevel: С какого уровня брать стек
        :return:
        """
        if kwargs.get('exc_info'):
            kwargs['exc_info'] = self.exc_info
        return self.log(DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        Добавляет сообщение уровня INFO

        :param msg: сообщение
        :param args: Дополнительные аргументы, которые будут использованы в сообщении
        :param exc_info: Если Истина то будет так же добавлена отладочная информация
        :param extra: Заносит дополнительную информацию, которую можно использовать в сообщение в дополнении к оладке
        :param stack_info: Если Истина добавляет стек
        :param stacklevel: С какого уровня брать стек
        :return:
        """
        if kwargs.get('exc_info'):
            kwargs['exc_info'] = self.exc_info
        return self.log(INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        Добавляет сообщение уровня WARNING

        :param msg: сообщение
        :param args: Дополнительные аргументы, которые будут использованы в сообщении
        :param exc_info: Если Истина то будет так же добавлена отладочная информация
        :param extra: Заносит дополнительную информацию, которую можно использовать в сообщение в дополнении к оладке
        :param stack_info: Если Истина добавляет стек
        :param stacklevel: С какого уровня брать стек
        :return:
        """
        if kwargs.get('exc_info'):
            kwargs['exc_info'] = self.exc_info
        return self.log(WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        Добавляет сообщение уровня ERROR

        :param msg: сообщение
        :param args: Дополнительные аргументы, которые будут использованы в сообщении
        :param exc_info: Если Истина то будет так же добавлена отладочная информация
        :param extra: Заносит дополнительную информацию, которую можно использовать в сообщение в дополнении к оладке
        :param stack_info: Если Истина добавляет стек
        :param stacklevel: С какого уровня брать стек
        :return:
        """
        if kwargs.get('exc_info'):
            kwargs['exc_info'] = self.exc_info
        return self.log(ERROR, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        Добавляет сообщение уровня CRITICAL

        :param msg: сообщение
        :param args: Дополнительные аргументы, которые будут использованы в сообщении
        :param exc_info: Если Истина то будет так же добавлена отладочная информация
        :param extra: Заносит дополнительную информацию, которую можно использовать в сообщение в дополнении к оладке
        :param stack_info: Если Истина добавляет стек
        :param stacklevel: С какого уровня брать стек
        :return:
        """
        if kwargs.get('exc_info'):
            kwargs['exc_info'] = self.exc_info
        return self.log(CRITICAL, msg, *args, **kwargs)

    def exception(self, msg, *args, trace=True, exc_info=True, stack_info=False, stacklevel=4, **kwargs):
        """
        Добавляет сообщение про исключение

        :param trace:
        :param msg: сообщение
        :param args: Дополнительные аргументы, которые будут использованы в сообщении
        :param exc_info: Если Истина то будет так же добавлена отладочная информация
        :param extra: Заносит дополнительную информацию, которую можно использовать в сообщение в дополнении к оладке
        :param stack_info: Если Истина добавляет стек
        :param stacklevel: С какого уровня брать стек
        :return:
        """
        if trace:
            msg = "{msg} {exception}".format(msg=msg, exception=traceback.format_exc())
        return self.error(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, **kwargs)
