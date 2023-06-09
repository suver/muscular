from .database import DBConnect, DBPool
from ..storage import StorageMapper
storageMapper = StorageMapper()


class MapperConstructor(object):
    """
    Конструктор мапера
    """

    def __init__(self, driver, name=None, as_default=False, meta=False):
        self.name = name
        self.driver = driver
        self.as_default = as_default
        self.meta = meta

    def __getattr__(self, name):
        driver = self.driver(self.name)
        if driver.hasmethod(name):
            return getattr(driver, name)
        raise AttributeError()


class DataMapper(MapperConstructor):
    """
    Объект для работы с БД
    """

    def connect(self, config=None) -> DBConnect:
        """
        Загружаем драйвер вызывая подключенный ранее класс self.driver как объект и подключаемся к бд

        :param config: Конфигурация подключения.

        :return: DBConnect
        """
        if config is None:
            config = {}
        pool = DBPool(self.driver)
        driver = self.driver(name=self.name)
        if self.name not in pool:
            connect = driver.connect(config=config)
            connect.as_default = self.as_default
            connect.meta = self.meta
            pool[self.name] = connect

        return pool[self.name]

    @staticmethod
    def driver(driver, name=None) -> object:
        """ Устанавливаем драйвер подключения к БД и передаем Имя подключения

        :param driver: Драйвера базы данных реализованную через интерфейс DataDriver.
        :param name: Наименование подключения.

        :return: DataMapper
        """
        return DataMapper(driver, name=name)


