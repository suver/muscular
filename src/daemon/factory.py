from typing import Dict, List
from ..core.cli import CliCommand
import threading
from .func import daemon as _daemon, DefaultThread
from functools import wraps


class Daemon(CliCommand):

    _daemons: List = []

    def __init__(self, key=None):
        self._key = key
        self._parent = None

    def add(self, daemon) -> None:
        self._daemons.append(daemon.__name__)
        daemon.parent = self

    def remove(self, daemon) -> None:
        self._daemons.remove(daemon.__name__)
        daemon.parent = None

    def execute(self, *args, **kwargs):
        pass

    def daemon(self, nums: int = 1, as_daemon: bool = False, wait_completion: bool = False):
        def decorator(func):
            daemonFactory.add(func, nums)
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            return wrapper
        return decorator


class DaemonFactory:

    _daemons = {}

    def __init__(self) -> None:
        pass

    def add(self, daemon, nums=1):
        daemon.__nums__ = nums
        self._daemons[daemon.__name__] = daemon
        return daemon

    def update(self, daemon):
        _daemon = self.set(daemon)
        return _daemon

    def get(self, daemon_name):
        return self._daemons.get(daemon_name)

    def set(self, daemon):
        self._daemons[daemon.__name__] = daemon
        return daemon

    def all(self) -> Dict:
        return self._daemons

    def items(self):
        return self._daemons.items()

    def list(self) -> None:
        count = len(self._daemons)
        print(f"DaemonFactory: I have {count} items:")
        for key in self._daemons:
            print(f"{key}", end="\n")
        print("\n")


daemonFactory = DaemonFactory()

daemon = Daemon()

