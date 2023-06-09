# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .__about__ import __version__, __description__
from .drivers.postgres import *
from .drivers.mysql import *
from .drivers.mongo import *
from .datamaper import *
from .database import *
from .migration import *
from .drivers.mysql import *
from .drivers.postgres import *
from .drivers.mongo import *
from .driver import *


class DataBase(object):
    """
    Создает подключение к базе данных для главной сущности фреймворка
    """

    def __init__(self, driver, config, name=None, as_default=False, meta=False):
        """
        Инициализирует подключение к базе данных.

        :param driver: see DataBaseDriver
        :param config: Конфигурация подключения
        :param name: Наименование подключение, может иметь значение None
        :param as_default: Если True то помечаем подключение как подключение по умолчанию.
        :param meta: Если True то помечаем подключение как подключение для мета данных. Важно помнить что одна база
                     данных может служить как база по умолчанию для всех данных, так же и для мета данных.
        """
        DataMapper(driver, name=name, as_default=as_default, meta=meta).connect(config=config)


__all__ = (
    "__version__",
    "__description__",
    "DataBase",
    "DBConnect",
    "DBPool",
    "DataMapper",
    "MongoDB",
    "Mysql",
    "Postgres",
)


