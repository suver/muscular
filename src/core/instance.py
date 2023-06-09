from __future__ import annotations
import sys
import os
import importlib
import inspect
import traceback

from .self import Prop
from ..wsgi import Request
from ..storage import StorageMapper


storageMapper = StorageMapper()


class Main:

    _instance = None
    ref = None

    def __new__(cls, *args, ref=None, **kwargs):
        if cls._instance is None:
            cls._instance = super(Main, cls).__new__(cls, *args, **kwargs)
            setattr(cls, 'ref', ref)
        return cls._instance

    def __init__(self, *args, ref=None, **kwargs):
        if ref is None:
            self.ref = ref

    def __set__(self, instance, ref):
        self.ref = ref

    def __get__(self, instance, owner):
        return self.ref


class MuscularSingletonMeta(type):
    """
    Реализация метакласса для создания на его основе экземпляра главного класса вашей программы

    """

    _instances = {}
    _args = ()
    _kwargs = {}

    def __call__(cls, *args, **kwargs):
        """
        Реализуем патерн одиночка

        :param args:
        :param kwargs:
        :return:
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(MuscularSingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def __init_subclass__(cls, *args, **kwargs):
        """


        :param args:
        :param kwargs:
        :return:
        """
        super().__init_subclass__()

        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')

        directory = os.getcwd()
        # Для примера создадим реестр всех наследников.
        # cls.registry.append(cls)

        if hasattr(cls, 'package_paths') and isinstance(cls.package_paths, list):
            for path in cls.package_paths:
                logger.debug(locale('Найден компонент {package}',
                                    package=f"{directory}/{path}"))
                sys.path.append(f"{directory}/{path}")
        elif hasattr(cls, 'package_paths') and isinstance(cls.package_paths, dict):
            for item in cls.package_paths:
                logger.debug(locale('Найден компонент {package}',
                                    package=f"{directory}/{cls.package_paths[item]}"))
                sys.path.append(f"{directory}/{cls.package_paths[item]}")

    def __new__(cls, class_name, parents, attributes, *args, **kwargs):
        """
        Модифицируем экземпляр класса, внедряя в него дополнительные возможности

        :param class_name:
        :param parents:
        :param attributes:
        """

        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        # Here we could add some helper methods or attributes to c
        c = type(class_name, parents, attributes)
        if not hasattr(c, 'locale'):
            logger.debug(locale('Создаем экземпляр {class_name}', class_name=class_name))
        setattr(c, 'import_package', cls.import_package)
        setattr(c, 'get_package_config', cls.get_package_config)
        setattr(c, 'init_auto_packages', cls.init_auto_packages)
        setattr(c, 'init_request', cls.init_request)
        setattr(c, 'init_imports', cls.init_imports)

        if hasattr(c, 'package_paths') and isinstance(c.package_paths, list):
            for item in c.package_paths:
                logger.debug(locale('Подключаем {item} => {packages}', item=item, packages=''.join(['init_', item])))
                setattr(c, ''.join(['init_', item]), cls.__init_structure(c, item))
        elif hasattr(c, 'package_paths') and isinstance(c.package_paths, dict):
            for item in c.package_paths:
                logger.debug(locale('Подключаем {item}', item=item))
                setattr(c, ''.join(['init_', item]), cls.__init_structure(c, item))

        main = Main(ref=c)
        return c

    def init_request(self):
        """
        Декоратор обработчика запросов

        :return:
        """
        def decorator(func):
            Request._before_start.append(func)
        return decorator

    def import_package(cls, package, config=None):
        """
        Предварительная реализация функции импортирующей пакеты.
        В основном классе может быть реализованая иная логика

        :param package: название пакета
        :param config: объект конфигурации пакета
        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')

        logger.debug(locale('Попытка загрузить пакет {package}', package=package))
        try:
            if package in sys.modules:
                logger.debug(locale('Пакет {package} уже загружен', package=package))
                module = sys.modules.get(package)
                module.__spec__.loader.exec_module(module)
            elif (spec := importlib.util.find_spec(package)) is not None:
                logger.debug(locale('Загружаем {package}', package=package))
                module = importlib.util.module_from_spec(spec)
                sys.modules[package] = module
                spec.loader.exec_module(module)
            else:
                logger.warning(locale('Пакет {package} не найден', package=package))
                return
            if config is not None:
                logger.debug(locale('Инициализируем {package} с настройками {config}',
                                    package=package, config=config))
                module.init_package(cls, config)
            # spec = importlib.util.find_spec('.', package=package)
            # print(spec.name)
            # # if importlib.util.find_spec(package) is not None:
            # logger.debug(locale('Загружаем {package}', package=package))
            # # _package = importlib.util.resolve_name('.', package=package)
            # # print(_package)
            # # _package = importlib.util.module_from_spec(spec)
            # # print(_package)
            # _package = importlib.__import__(spec.name, globals(), locals(), [], 0)
            # # _package = importlib.import_module(spec.name)
            # print(_package)
            # try:
            #     if config is not None:
            #         _package.init_package(cls, config)
            #         logger.debug(locale('Инициализируем {package} с настройками {config}',
            #                             package=package, config=config.__dict__))
            # except Exception as e:
            #     # tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            #     # traceback.print_exc()
            #     logger.exception(locale('Ошибка импорта пакета'))
            # except IndentationError as e:
            #     # tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
            #     # traceback.print_exc()
            #     logger.exception(locale('Ошибка импорта пакета'))
        except Exception as e:
            traceback.print_exc()
            logger.warning(locale('Пакет {package} не найден', package=package))

    def get_package_config(self, package_obj: dict, init_key=None):
        """
        Преобразуем конфигурацию пакета

        :param package_obj: конфигурация пакета
        :param init_key: ключ пакета
        :return:
        """
        locale = storageMapper.get('locale')
        if not package_obj:
            raise Exception(locale('Конфигурация пакета не указана'))
        if init_key is not None and 'key' not in package_obj:
            package_obj['key'] = init_key
        if 'url_prefix' not in package_obj:
            package_obj['url_prefix'] = '/' + package_obj['key']
        if 'templates' not in package_obj:
            package_obj['templates'] = 'templates'
        if 'static' not in package_obj:
            package_obj['static'] = 'static'
        return package_obj

    def __init_structure(self, package_structure):
        def init_structure(self, config):
            for init_key in config[package_structure]:
                package = config[package_structure][init_key]
                self.import_package(package['package'], self.get_package_config(package, init_key=init_key))
        return init_structure

    def init_auto_packages(self, config, package_paths=None):
        """
        Импортируем все пакеты указанные в настройках

        :param package_paths:
        :param config: объект конфигурации
        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        logger.debug(locale('Загружаем пакеты'))
        if package_paths is None:
            package_paths = self.package_paths or []
        for item in package_paths:
            logger.debug(locale('Обработка пакета {package}', package=item))
            if item not in config:
                logger.debug(locale('Конфигурация пакета {package} не найдена', package=item))
                continue
            for init_key in config[item]:
                logger.debug(locale('Подключаем пакет {package} {init_key}', package=item, init_key=init_key))
                package = config[item][init_key]
                self.import_package(package['package'], config=self.get_package_config(package, init_key=init_key))

    def init_imports(self, config):
        """
        Импортируем все пакеты указанные в настройках

        :param config: объект конфигурации
        :return:
        """
        for init_key in config:
            package = config[init_key]
            self.import_package(package)


class PackageMeta(type):
    """
    Метакласс для создания объекта пакета

    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Реализуем патерн одиночка

        :param args:
        :param kwargs:
        :return:
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(PackageMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__()
        directory = os.getcwd()
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        logger.debug('PackageMeta.__init_subclass__ {directory}'.format(directory=directory))
        if hasattr(cls, 'package_paths') and isinstance(cls.package_paths, list):
            for path in cls.package_paths:
                sys.path.append(f"{directory}/{path}")
        elif hasattr(cls, 'package_paths') and isinstance(cls.package_paths, dict):
            for item in cls.package_paths:
                sys.path.append(f"{directory}/{cls.package_paths[item]}")

    def __new__(cls, class_name, parents, attributes):
        """
        Модифицируем экземпляр класса, внедряя внего дополнительные возможности

        :param class_name:
        :param parents:
        :param attributes:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        logger.debug(locale('Создаем экземпляр {class_name}', class_name=class_name))
        # Here we could add some helper methods or attributes to c
        c = type.__new__(cls, class_name, parents, attributes)
        sys_directory = os.getcwd()
        directory = os.path.dirname(os.path.realpath(inspect.getfile(c)))
        setattr(c, 'sys_directory', sys_directory)
        setattr(c, 'directory', directory)
        setattr(c, 'import_package', cls.import_package)
        setattr(c, 'get_package_config', cls.get_package_config)
        setattr(c, 'init_auto_packages', cls.init_auto_packages)
        for name, attr in attributes.items():
            if inspect.isclass(type(attr)) and isinstance(attr, Prop):
                setattr(attr, 'app', c)

        if hasattr(c, 'package_paths') and isinstance(c.package_paths, list):
            for item in c.package_paths:
                sys.path.append(f"{directory}/{item}")
                logger.debug(locale('Подключаем {item} => package', item=item, package=''.join(['init_', item])))
                setattr(c, ''.join(['init_', item]), cls.__init_structure(c, item))
        elif hasattr(c, 'package_paths') and isinstance(c.package_paths, dict):
            for item in c.package_paths:
                sys.path.append(f"{directory}/{cls.package_paths[item]}")
                logger.debug(locale('Подключаем {item}', item=item))
                setattr(c, ''.join(['init_', item]), cls.__init_structure(c, item))

        return c

    def import_package(cls, package, config):
        """
        Предварительная реализация функции импортирующей пакеты. В основном классе может быть реализованая иная логика

        :param package: название пакета
        :param config: объект конфигурации пакета
        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        dir_list = package.split('.')
        spec = importlib.util.spec_from_file_location(package, '/'.join([cls.directory] + dir_list + ['__init__.py']))
        if spec is not None:
            logger.debug(locale('Импортируем пакет {package}', package=package))
            # _package = importlib.import_module(package)
            _package = spec.loader.load_module()
            try:
                _package.init_package(cls, config)
                logger.debug(locale('Инициализируем пакет {package}', package=package))
            except Exception as e:
                # tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
                # print('!!!ERROR: ', "\n".join(tb_str))
                # traceback.print_exc()
                logger.exception(locale('Ошибка импорта пакета'))
            except IndentationError as e:
                # tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
                # print('!!!ERROR: ', "/n".join(tb_str))
                # traceback.print_exc()
                logger.exception(locale('Ошибка импорта пакета'))
        else:
            logger.warning(locale('Пакет {package} не найден', package=package))

    def get_package_config(self, package_obj: dict, init_key=None):
        """
        Преобразуем конфигурацию пакета

        :param package_obj: конфигурация пакета
        :param init_key: ключь пакета
        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if not package_obj:
            raise Exception(locale('Конфигурация пакета не найдена'))
        if init_key is not None and 'key' not in package_obj:
            package_obj['key'] = init_key
        if 'url_prefix' not in package_obj:
            package_obj['url_prefix'] = '/' + package_obj['key']
        if 'templates' not in package_obj:
            package_obj['templates'] = 'templates'
        if 'static' not in package_obj:
            package_obj['static'] = 'static'
        return package_obj

    def __init_structure(self, package_structure):
        def init_structure(self, config):
            for init_key in config[package_structure]:
                package = config[package_structure][init_key]
                self.import_package(package['package'], self.get_package_config(package, init_key=init_key))
        return init_structure

    def init_auto_packages(self, config):
        """
        Импортируем все пакеты указанные в настройках

        :param config: объект конфигурации
        :return:
        """
        for item in self.package_paths:
            if item not in config:
                continue
            for init_key in config[item]:
                package = config[item][init_key]
                self.import_package(package['package'], self.get_package_config(package, init_key=init_key))
