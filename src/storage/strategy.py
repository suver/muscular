import typing
from abc import ABC


class StorageStrategy(ABC):
    """
    Стратегия конструктора объекта перед возвращением его из хранилища.
    ВАЖНО: Объект создается каждый раз из класса находящегося в хранилище

    """

    def __init__(self, cls):
        self.cls = cls

    def construct(self) -> typing.Any:
        """
        Непосредственно конструктор объекта из класса в хранилище

        :return:
        """
        if type(self.cls) == tuple:
            return self.cls[0](*self.cls[1], **self.cls[2])
        else:
            return self.cls()

