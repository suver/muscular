from typing import Union
from .database import DBPool
from ..models import Collection, Column
from ..storage import StorageMapper
storageMapper = StorageMapper()


class LinkDriver(object):
    """
    Link объекты предназначены для добавления к драйверам новых возможностей.
    Например, подключение к бд, создание схем внутри бд, выполнении запросов и тд.
    """

    def __init__(self, instance):
        self.instance = instance


class DatabaseLinkDriver(LinkDriver):
    """
    Link объекты предназначены для добавления к драйверам новых возможностей.
    Например, подключение к бд, создание схем внутри бд, выполнении запросов и тд.
    """
    pass


class DataDatabaseLinkDriver(LinkDriver):
    """
    Данные для работы с БД
    """

    def __init__(self, instance):
        super().__init__(instance)
        self.instance._collection = None
        self.instance._column = None
        self.instance._model = None

    def collection(self, collection):
        if isinstance(collection, Collection):
            self.instance._collection = collection
        elif isinstance(collection, str):
            self.instance._collection = Collection(collection)
        return self.instance

    def column(self, column):
        if isinstance(column, Column):
            self.instance._column = column
        elif isinstance(column, str):
            self.instance._column = Column(column)
        return self.instance

    def model(self, model):
        self.instance._model = model
        return self.instance


class DriverConstructor(object):
    """
    Интерфейс для драйверов баз данных

    """

    def __new__(cls, name=None, *args, **kwargs):
        """
        Реализация потерна "одиночка". Если соединение уже присутствует в базе данных, то используем именно его

        :param args:
        :param name: Название соединения.
        :param kwargs:
        """
        pool = DBPool(cls)
        return pool[name] if name in pool else super().__new__(cls)


class CRUDDatabaseLinkDriver(DatabaseLinkDriver):
    """
    Link объект для управления схемами БД
    """

    def create(self, collection_name=None, after=None) -> Union[Exception, bool]:
        """
        Умный метод добавления в базу данных сущностей опираясь на метаданные модели.

        :param collection_name: Названье коллекции.
        :param after: Добавить после.
        :return:
        """
        try:

            if collection_name is None and isinstance(self.instance._collection, Collection):
                collection_name = self.instance._collection.collection_name
            if isinstance(self.instance._collection, Collection) and not isinstance(self.instance._column, Column):
                return self.instance.add_collection()
            elif isinstance(self.instance._column, Column):
                return self.instance.add_column(collection_name=collection_name, after=after)
        except Exception as e:
            locale = storageMapper.get('locale')
            logger = storageMapper.get('logger')
            logger.exception(locale('Ошибка %s.create()', self.instance.__class__.__name__))
            raise e

    def drop(self, collection_name=None, column_name=None) -> Union[Exception, bool]:
        """
        Умный метод удаления сущностей из базы данных опираясь на переданные аргументы

        :param collection_name: Имя коллекции.
        :param column_name: Имя поля в коллекции. Если поле не передано будет удалена вся коллекция.
        :return:
        """
        try:
            if collection_name is None:
                collection_name = self.instance._collection.collection_name
            if collection_name is not None and column_name is None:
                return self.instance.drop_collection(collection_name=collection_name)
            if collection_name is not None and column_name is not None:
                return self.instance.drop_column(collection_name=collection_name, column_name=column_name)
        except Exception as e:
            locale = storageMapper.get('locale')
            logger = storageMapper.get('logger')
            logger.exception(locale('Ошибка %s.drop()', self.instance.__class__.__name__))
            raise e


class DataDriver(DriverConstructor):
    """
    Пример драйвера для БД
    """

    def __init__(self, name=None):
        self.name = name
        self._mappers = []

    def __getattr__(self, name):
        for mapper in self._mappers:
            if hasattr(mapper, name):
                return getattr(mapper, name)
            else:
                pass
        raise AttributeError(name)

    def hasmethod(self, name):
        """
        Возвращает Истина если метод присутствует в одном из Link объектов
        """
        for mapper in self._mappers:
            if hasattr(mapper, name):
                return True
        return False