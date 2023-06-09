from ..core.strategy import Strategy
import os
import sys
from typing import List
from ..console.colory import Colors
from .factory import daemonFactory, daemon
from .func import DefaultThread, StopThread, WaitThread


class flushfile(object):
  def __init__(self, f):
    self.f = f

  def write(self, x):
    pass

  def flush(self):
    pass


class DaemonStrategy(Strategy):

    try:
        rows, columns = os.popen('stty size', 'r').read().split()
    except:
        rows = 50
        columns = 100

    def print_header(self):
        author = '(c) Butko Denis'
        lines = [
            '-' * (int(self.columns) - 4),
            'Muscular',
            'Daemon',
            author.rjust(int(self.columns)-len(author)),
            '-' * (int(self.columns) - 4),
        ]
        for line in lines:
            print(f"{Colors.HEADER}--{line.center(int(self.columns)-4)}--{Colors.ENDC}")

    def execute(self, *args, shutup=False, **kwargs) -> List:
        if not shutup:
            self.print_header()
        else:
            sys.stdout = flushfile(sys.stdout)

        # daemonFactory.list()
        daemons = daemonFactory.all()

        threads = {}
        while True:
            try:
                for key in daemons:
                    nums = daemons[key].__nums__ if daemons[key].__nums__ else 1
                    for i in range(nums):
                        try:
                            name = f"{daemons[key].__name__}-{i}"
                            if name not in threads:
                                threads[name] = DefaultThread(daemons[key])
                                # print(f"create {key}")
                            if not threads[name].is_alive() and threads[name].action == 'active':
                                threads[name] = DefaultThread(daemons[key])
                                threads[name].start()
                                # print(f"is run {threads[key].name}")
                            elif threads[name].action == 'stop':
                                raise StopThread(name)
                            elif threads[name].action == 'wait':
                                raise WaitThread(name)
                            else:
                                # print('is alive')
                                pass
                        except WaitThread:
                            continue
            except KeyboardInterrupt:
                break
            except StopThread:
                break

