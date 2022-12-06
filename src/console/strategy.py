from ..core.strategy import Strategy
import os
import sys
from typing import List
from .colory import Colors
from .instance import cli
from ..storage import StorageMapper
storageMapper = StorageMapper()


class flushfile(object):
  def __init__(self, f):
    self.f = f

  def write(self, x):
    pass

  def flush(self):
    pass


class CliStrategy(Strategy):
    """
    Стратегия для контекста переводящая обработку в режим работы в консоли

    """

    try:
        rows, columns = os.popen('stty size', 'r').read().split()
    except:
        rows = 50
        columns = 100

    def print_header(self):
        """
        Печатаем базовый заголовок в консоли

        :return:
        """
        author = '(c) Butko Denis'
        lines = [
            '-' * (int(self.columns) - 4),
            'Muscular',
            'CLI',
            author.rjust(int(self.columns)-len(author)),
            '-' * (int(self.columns) - 4),
        ]
        for line in lines:
            print(f"{Colors.HEADER}--{line.center(int(self.columns)-4)}--{Colors.ENDC}")

    def execute(self, *args, shutup=False, **kwargs) -> List:
        """
        Первичный обработчик консольных команд

        :param args:
        :param shutup: приглушаем весь вывод в stdout
        :param kwargs:
        :return:
        """
        if not shutup:
            self.print_header()
        else:
            sys.stdout = flushfile(sys.stdout)
        if len(args) <= 0:
            args = sys.argv[1:]
        result = cli.execute(*args, {})
        return result

