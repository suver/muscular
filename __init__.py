# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .__about__ import __version__, __description__
import os

from .src.storage import StorageMapper
from .src.logging.logger import Logger
from .src.locale.locale import Locale

storageMapper = StorageMapper()
storageMapper.add('logger', Logger, 'framework')

storageMapper.add('locale', Locale,
                  name='framework',
                  install=False,
                  domain='message',
                  languages=['en', 'ru'],
                  directory=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'locales')),
                  fallback=True,
                  translate_functions=['locale', 't'],
                  babelrc=None,
                  default_language='ru'
                  )
from .src.locale.cmd import *
from .src.core.context import Context, Strategy
from .src.core.instance import MuscularSingletonMeta, PackageMeta, Main
from .src.core.metaclass import SingletonMeta
from .src.wsgi import WsgiStrategy, routes, Routes
from .src.console import *
from .src.daemon import DefaultThread, DaemonStrategy, daemon, daemonFactory
from .src.configuration import *
from .src.data import *
from .src.core import *
from .src.console import *
from .src.template import *
from .src.wsgi import *
from .src.logging import *
from .src.locale.locale import *
from .src.models import *
from .src.watchdog import *
from .src.uwsgi import *
from .src.template import *
from .src.restful import *
# from .src.models import *
from .src.schema import *
from .src.schema import Json


__all__ = (
    "__version__",
    "__description__",
    "DaemonStrategy",
    "daemonFactory",
    "DefaultThread",
    "daemon",
    "Swagger",
    "BaseParameter",
    "HeaderParameter",
    "CookieParameter",
    "PathParameter",
    "QueryParameter",
    "FormParameter",
    "File",
    "ResponseBody",
    "JsonResponseBody",
    "XmlResponseBody",
    "EmptyResponseBody",
    "TextResponseBody",
    "RequestBody",
    "JsonRequestBody",
    "XmlRequestBody",
    "FormRequestBody",
    "MultipartRequestBody",
    "FileRequestBody",
    "PayloadRequestBody",
    "RestApi",
    "Template",
    "ModelStorage",
    "TemplateLoader",
    "ExceptionHandler",
    "UwsgiReload",
    "Watchdog",
    "PatternMatchingHandler",
    "Self",
    "Configurator",
    "DataBase",
    "CliStrategy",
    "Locale",
    "cli",
    "Logger",
    "message",
    "BaseModel",
    "Model",
    "DataBase",
    "DBConnect",
    "DBPool",
    "DataMapper",
    "MongoDB",
    "Mysql",
    "Postgres",

    "BaseGroup",
    "Group",
    "ModelStorage",
    "Model",
    "Boolean",
    "List",
    "Email",
    "Phone",
    "Time",
    "Enum",
    "Float",
    "Numeric",
    "Binary",
    "String",
    "Json",
    "SmallInteger",
    "Integer",
    "Date",
    "Column",
    "Collection",
    "Text",
    "DateTime",
    "Timestamp",
    "BigInteger",
    "Key",

    "Context",
    "Strategy",
    "MuscularSingletonMeta",
    "Main",
    "PackageMeta",
    "SingletonMeta",
    "routes",
    "Routes",

    "WsgiStrategy",
    "Api",
    "api"
)
