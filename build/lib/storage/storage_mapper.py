import traceback
import typing
from .storage import Storage
from .strategy import StorageStrategy


class StorageMapper:
    """
    Класс создания объекта для работы с хранилизами

    Шаг 1: Инициализируем хранилизе

    os = StorageMapper()

    -- или --

    os = StorageMapper(strategy=Strategy, storage=Storage)

    -- или --

    os = StorageMapper()
    os.strategy = Strategy
    os.storage = Storage

    Шаг 2: Устанавливаем в хранилище класс объект

    class TestConstruct(metaclass=SingletonMeta):
        def __init__(self):
            self.val = 1

    os['test'] = TestConstruct

    -- или --

    class Test2Construct():
        def __init__(self):
            self.val = 2

    os.add('test2', Test2Construct)

    -- или --

    class Test3Construct(TestConstruct):
        def __init__(self, val):
            self.val = val

    os.add('test3', Test3Construct, 13, instance=TestConstruct)

    os.get('test3')

    class Test5Construct(TestConstruct):
        def __init__(self, val):
            self.val = val

    os.upg('test3', Test5Construct)

    os.get('test3')

    -- или --

    class Test4Construct:
        def __init__(self, val, name=None):
            self.val = val
            self.name = name

    os.add('test4', Test4Construct, 14, name='Vasily')

    os.add('test2', Test2Construct)

    """

    def __init__(self, strategy: StorageStrategy = None, storage: Storage = None) -> None:
        """
        Конструктор класса для работы с хранилизами
        """
        if strategy is None:
            strategy = StorageStrategy
        if storage is None:
            storage = Storage
        self.strategy = strategy
        self.storage = storage

    @property
    def strategy(self) -> StorageStrategy:
        """
        Вернет текущую стратегию
        """
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: StorageStrategy) -> None:
        """
        Установит текущую стратегию
        """
        if not issubclass(strategy, StorageStrategy):
            raise Exception(
                'ObjectStorage.strategy = %s -> The class is not an instance %s' % (strategy, StorageStrategy))
        self._strategy = strategy

    @property
    def storage(self) -> Storage:
        """
        Вернет текущее хранилище
        """
        return self._storage

    @storage.setter
    def storage(self, storage: Storage) -> None:
        """
        Установит текущее хранилище
        """
        if not issubclass(storage, Storage):
            raise Exception('ObjectStorage.storage = %s -> The class is not an instance %s' % (storage, Storage))
        self._storage = storage

    def __setitem__(self, key, value):
        """
        Провайдер для установки класса объекта в хранилище

        :param key: Ключ
        :param value: Класс
        :return:
        """
        obj = self._storage()
        obj[key] = value

    def __getitem__(self, key) -> typing.Any:
        """
        Провайдер который достает и конструирует объект из класса в хранилище

        :param key: Ключ
        :return:
        """
        obj = self._storage()
        if key not in obj:
            traceback.print_stack()
            raise Exception('ObjectStorage.__getitem__(%s, %s) -> Not Found' % (obj, key))
        st = self._strategy(obj[key])
        return st.construct()

    def __contains__(self, key):
        """
        Провайдер для проверки наличия класса в хранилище

        :param key:
        :return:
        """
        obj = self._storage()
        return key in obj

    def add(self, key, value, *args, instance=None, ignore_if_exists=False, **kwargs):
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
        if key in self and ignore_if_exists == False:
            raise Exception('ObjectStorage.add(%s, %s) -> Key already added' % (key, value))
        self[key] = (value, args, kwargs, instance)

    def upg(self, key, value):
        """
        Обновляет класс по ключу в хранилище и при этом сохраняет старые значения конструктора

        :param key: Ключ
        :param value: Класс
        :return:
        """
        obj = self._storage()
        st = getattr(obj, key)
        if st[3] is not None and not issubclass(value, st[3]):
            raise Exception('ObjectStorage.upg(%s, %s) -> The class is not an instance %s' % (key, value, st[3]))
        self[key] = (value, st[1], st[2])

    def get(self, key):
        """
        Вернет класс объекта из хранилища.
        Рекомендуется к использованию вместо обращения os[key]

        :param key:
        :return:
        """
        try:
            return self[key]
        except Exception:
            return None
