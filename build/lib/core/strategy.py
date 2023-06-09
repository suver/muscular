from __future__ import annotations
from abc import ABC, abstractmethod
from ..storage import StorageMapper
storageMapper = StorageMapper()


class Strategy(ABC):
    """
    Интерфейс Стратегии объявляет операции, общие для всех поддерживаемых версий
    некоторого алгоритма.

    Контекст использует этот интерфейс для вызова алгоритма, определённого
    Конкретными Стратегиями.
    """

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
