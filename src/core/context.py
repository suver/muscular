from __future__ import annotations
from abc import abstractmethod
from functools import wraps
from .strategy import Strategy
from ..core.metaclass import SingletonMeta
from ..storage import StorageMapper

storageMapper = StorageMapper()



class Context(metaclass=SingletonMeta):
    """
    Контекст определяет интерфейс, представляющий интерес для клиентов.
    """

    before_start_function_list = []
    after_start_function_list = []
    context_function_list = []
    _params = {}

    def __init__(self, strategy: Strategy, options: dict, params: dict = {}) -> None:
        """
        Обычно Контекст принимает стратегию через конструктор, а также
        предоставляет сеттер для её изменения во время выполнения.
        """
        self._strategy = strategy
        if not options:
            options = {}
        if not params:
            params = {}
        self._owner = None
        self._params.update(params)
        self._params.update(options)

    def __set_name__(self, owner, name):
        self._name = name
        self.set_container(owner)

    def set_container(self, owner):
        """
        Устанавливаем объект в контейнер контекста

        :param owner: объект контекста
        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        logger.debug(locale("Устанавливаем контекст в свойство {name} объекта {owner}",
            name=self._name,
            owner=str(owner)
        ))
        self._owner = owner

    @abstractmethod
    def before_start(self):
        """
        Обработчик before_start

        :return:
        """
        def decorator(func):
            self.before_start_function_list.append(func)

            locale = storageMapper.get('locale')
            logger = storageMapper.get('logger')
            logger.debug(locale("Устанавливаем обработчик before_start {handler}. {doc}",
                doc=func.__doc__ if func.__doc__ else '',
                handler=str(func)
            ))
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            return wrapper
        return decorator

    @abstractmethod
    def after_start(self):
        """
        Обработчик after_start

        :return:
        """
        def decorator(func):
            self.after_start_function_list.append(func)

            locale = storageMapper.get('locale')
            logger = storageMapper.get('logger')
            logger.debug(locale("Устанавливаем обработчик after_start {func}. {doc}",
                doc=func.__doc__ if func.__doc__ else '',
                func=str(func)
            ))
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            return wrapper
        return decorator

    @abstractmethod
    def context(self):
        """
        Обработчик context

        :return:
        """
        def decorator(func):
            self.context_function_list.append(func)

            locale = storageMapper.get('locale')
            logger = storageMapper.get('logger')
            logger.debug(locale("Устанавливаем обработчик context {func}. {doc}",
                doc=func.__doc__ if func.__doc__ else '',
                func=str(func)
            ))
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            return wrapper
        return decorator

    def add_param(self, key, value):
        if self._params.get(key, False):
            locale = storageMapper.get('locale')
            raise Exception(locale('Невозможно установить %s, параметр уже установлен', key))
        self._params[key] = value

    def set_param(self, key, value):
        self._params[key] = value

    def param(self, key):
        if not self._params.get(key, False):
            locale = storageMapper.get('locale')
            raise Exception(locale('Невозможно получить %s, параметр не существует', key))
        return self._params[key]

    @property
    def strategy(self) -> Strategy:
        """
        Контекст хранит ссылку на один из объектов Стратегии. Контекст не знает
        конкретного класса стратегии. Он должен работать со всеми стратегиями
        через интерфейс Стратегии.
        """
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        """
        Обычно Контекст позволяет заменить объект Стратегии во время выполнения.
        """

        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        logger.debug(locale("Устанавливаем новую стратегию {strategy}. {doc}",
            doc=strategy.__doc__ if strategy.__doc__ else '',
            strategy=str(strategy)
        ))
        self._strategy = strategy

    def execute(self, *args, **kwargs) -> str:
        """
        Вместо того, чтобы самостоятельно реализовывать множественные версии
        алгоритма, Контекст делегирует некоторую работу объекту Стратегии.
        """
        '''Запускаем обработчики before_start'''
        for func in self.before_start_function_list:
            func(self._owner)
        '''Запускаем обработчики context'''
        for func in self.context_function_list:
            func(self._owner, self)

        strategy = self.strategy()
        kwargs.update(self._params)
        kwargs.update({'container': self._owner})
        result = strategy.execute(*args, **kwargs)

        '''Запускаем обработчики after_start'''
        for func in self.after_start_function_list:
            func(self._owner, result)
        return result
