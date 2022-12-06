from ..core.metaclass import SingletonNamedMeta
from ..storage import StorageMapper
storageMapper = StorageMapper()


class DBConnect(object):
    """
    Соединение с базой данных
    """

    _url = None
    connection = None
    engine = None
    session = None
    driver = None
    as_default = False
    meta = False
    ctx = None


class DBPool(metaclass=SingletonNamedMeta):
    """
    На основе этого класса создается хранилище подключений к базе данных.

    '''
    # Получаем список подключений к БД для драйвера Postgres.
    pool = DBPool(Postgres)

    # Таким образом можно получить конкретное именованное подключение.
    if self.name in pool:
        self.c = pool[self.name]
        return pool[self.name]
    '''

    """

    storage = dict()
    keys = dict()

    def __init__(self, connect, *args, **kwargs):
        """
        Заносим подключение в хранилище

        :param DBConnect connect: Подключение к базе данных
        """
        self.cur = 0
        self.connect = connect
        if str(connect) not in self.storage:
            self.storage[str(connect)] = dict()
            if str(connect) not in self.keys:
                self.keys[str(self.connect)] = []
            self.keys[str(self.connect)].append(str(connect))

    def get_connect(self, key=None) -> DBConnect:
        """
        Возвращает подключение к базе данных. Если параметр key не указан, вернем значение по умолчанию

        :param key: Название подключения.
        :raise: IndexError
        :return: DBConnect
        """
        if key is None:
            key = 'default'
        if str(key) in self.storage[str(self.connect)]:
            return self.storage[str(self.connect)][str(key)]
        else:
            raise IndexError

    def cursor(self) -> DBConnect:
        """
        Возвращает текущее итерируемое подключение к базе данных.

        pool = DBPool(Postgres)
        connect1 = next(pool) # берем следующее значение итератора
        connect2 = pool.cursor() # берем текущее значение итератора, таким образом connect1 == connect2

        :return: DBConnect
        """
        return self.storage[str(self.connect)][self.keys[self.cur]]

    def __contains__(self, key) -> bool:
        """
        Определить механизм проверки наличия элемента в объекте-контейнере.

        'connection_name' in pool

        :param key: Элемент, наличие которого в объекте требуется определить.
        :return: bool
        """
        if key is None:
            key = 'default'
        return str(key) in self.storage[str(self.connect)]

    def __iter__(self) -> iter:
        """
        Определить механизм прохода (итерирования) по элементам объекта

        :return: iter
        """
        return iter(self.storage[str(self.connect)].items())

    def __repr__(self) -> str:
        """
        repr()

        :return: str
        """
        return str(self.storage[str(self.connect)])

    def __next__(self) -> DBConnect:
        """
        Очерёдность прохода по элементам объекта
        next()

        :return: DBConnect
        """
        if self.cur == len(self.keys):
            raise StopIteration
        self.cur = self.cur + 1
        return self.storage[str(self.connect)][self.keys[self.cur]]

    def __setitem__(self, key, value) -> None:
        """
        Добавление соединения с базой данных в хранилище

        pool['connection_name'] = DBConnect(config)

        :param key: Ключ, которым адресуется элемент контейнера.
        :param value: Значение, которое ставится в соответствие указанному ключу.
        :return: None
        """
        if key is None:
            key = 'default'
        self.storage[str(self.connect)][str(key)] = value
        self.keys[str(self.connect)].append(str(key))

    def __delitem__(self, key) -> None:
        """
        Удаляет подключение из хранилища

        del container['connection_name']

        :raise IndexError
        :param key:
        :return: None
        """
        if key is None:
            key = 'default'
        if str(key) in self.storage[str(self.connect)]:
            del self.storage[str(self.connect)][str(key)]
            self.keys[str(self.connect)].remove(str(key))
        else:
            raise IndexError

    def __getitem__(self, key) -> DBConnect:
        """
        Обращении к элементу контейнера.

        my_container['connection_name']

        :raise IndexError
        :param key:
        :return: DBConnect
        """
        if key is None:
            key = 'default'
        if str(key) in self.storage[str(self.connect)]:
            return self.storage[str(self.connect)][str(key)]
        else:
            raise IndexError

    def __add__(self, item) -> dict:
        """
        Позволяет добавлять к хранилищу новое соединение операцией сложения

        DBPool(Postgres) + DBConnect(config)

        :param item: DBConnect
        :return: dict
        """
        return self.storage[str(self.connect)] + {str(len(self.storage[str(self.connect)]) + 1): item}



