

class SingletonMeta(type):
    """
    Метакласс позволяющий превратить ваш класс в одиночку путем добавления этого метакласса

    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Данная реализация не учитывает возможное изменение передаваемых
        аргументов в `__init__`

        :param args:
        :param kwargs:
        :return:
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SingletonNamedMeta(type):
    """
    Метакласс позволяющий превратить ваш класс в одиночку путем добавления этого метакласса. Для определения
    приналежности объекта используется также идентификатор имени `name`

    """

    _instances = {}

    def __call__(cls, *args, name: str = None, **kwargs):
        """
        Данная реализация не учитывает возможное изменение передаваемых
        аргументов в `__init__`.

        :param name:
        :param args:
        :param kwargs:
        :return:
        """
        key = '-'.join([str(cls), str(name)])
        if key not in cls._instances:
            kwargs['name'] = name
            instance = super().__call__(*args, **kwargs)
            cls._instances[key] = instance
        return cls._instances[key]
