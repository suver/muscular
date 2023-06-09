from ..core.metaclass import SingletonNamedMeta


class BaseModel(object):

    registry = []

    def __getstate__(self):
        return {'special_x': self.x}

    def __setstate__(self, state):
        self.x = state['special_x']

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__()
        cls.registry.append(cls)


class Model(BaseModel):
    __metaclass__ = BaseModel
    __prefix__ = ""
    __collection__ = None

    def __init__(self, *args, **kwargs):
        self.collection = "{prefix}{collection}".format(
            collection=self.__collection__ if self.__collection__ else self.__class__.__name__.lower(),
            prefix="%s_" % self.__prefix__ if self.__prefix__ else ''
        )
        if len(kwargs) > 0 and hasattr(self, 'columns'):
            for column in self.columns:
                self.columns[column].value = kwargs.get(column) or self.columns[column].default or None

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__()
        ms = ModelStorage()
        ms[cls.__name__] = cls


class ModelStorage(metaclass=SingletonNamedMeta):

    def __init__(self, *args, **kwargs) -> None:
        """
        Конструктор класса для работы с хранилизами
        """
        if not hasattr(self, '_models'):
            self._models = {}

    @property
    def models(self) -> dict:
        """
        Вернет текущее хранилище
        """
        return self._models

    def __setitem__(self, key, value):
        """
        Провайдер для установки класса объекта в хранилище

        :param key: Ключ
        :param value: Класс
        :return:
        """
        self._models[key] = value

    def __getitem__(self, key) -> Model:
        """
        Провайдер который достает и конструирует объект из класса в хранилище

        :param key: Ключ
        :return: Model
        """
        return self._models[key]

    def __contains__(self, key):
        """
        Провайдер для проверки наличия класса в хранилище

        :param key:
        :return:
        """
        return key in self._models

    def add(self, key, value):
        """
        Заносит класс объекта в хранилище с дополнительными проверками.
        Рекомендуется к использованию вместо обращения os[key] = class

        :param key: Ключ
        :param value: Класс
        :param args: Аргументы для передачи конструктору
        :param instance: Клас для проверки принадлежности
        :param kwargs: словарь для передачи конструктору объекта
        :return:
        """
        if key in self._models:
            raise Exception('ObjectStorage.add(%s, %s) -> Key already added' % (key, value))
        self._models[key] = value

    def get(self, key) -> Model:
        """
        Вернет класс объекта из хранилища.
        Рекомендуется к использованию вместо обращения os[key]

        :param key:
        :return: Model
        """
        return self._models.get(key, None)
