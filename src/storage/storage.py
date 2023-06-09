
class Storage(object):
    """
    Класс хранилища созданный на основе патерна одиночка. Каждый раз при создании объекта мы получаем одиин и
    тот же его экзепляр.

    """
    _instances = {}

    def __new__(cls, *args, **kwargs):
        """
        Данная реализация не учитывает возможное изменение передаваемых
        аргументов в `__init__`

        :param args:
        :param kwargs:
        :return:
        """
        if cls not in cls._instances:
            instance = super().__new__(cls, *args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self):
        if not hasattr(self, 'storage'):
            self.storage = {}

    def __setitem__(self, key, value):
        """
        Заносит в словарь хранилища новый класс

        :param key: Ключ
        :param value: Объект
        :return:
        """
        self.storage[key] = value

    def __getitem__(self, key):
        """
        Достает класс из словаря по ключу

        :param key: Ключ
        :return:
        """
        return self.storage[key] or None

    def __contains__(self, key):
        """
        Проверяет находится ли класс в хранилище

        :param key: Ключ для поиска
        :return:
        """
        return key in self.storage

    def exists(self, key):
        """
        Проверка наличия класса в хранилище

        :param key: Ключ для поиска
        :return:
        """
        return key in self.storage
