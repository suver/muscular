from __future__ import annotations
import threading
import getpass
from threading import Thread


def argsparse(arguments, args):
    '''@TODO переписать логику'''
    kwargs = {}
    for argument in arguments:
        if argument.nargs > 1 or argument.multiple:
            kwargs[argument.dest] = []
        else:
            kwargs[argument.dest] = argument.default
        _args = iter(args)
        arg = next(_args, False)
        while arg:
            next_arg = next(_args, False)
            if arg == argument.argument or arg == argument.short:
                if argument.nargs <= 0:
                    '''Обрабатываем флаги'''
                    kwargs[argument.dest] = argument.flag_value
                elif argument.nargs == 1:
                    '''Обрабатываем элемент со значением'''
                    value = False if next_arg and next_arg[0:1] == '-' else next_arg
                    if value:
                        if argument.multiple:
                            kwargs[argument.dest].append(value)
                        else:
                            kwargs[argument.dest] = value
                    if argument.prompt and not kwargs[argument.dest] and argument.password:
                        kwargs[argument.dest] = getpass.getpass(
                            f"{argument.prompt if argument.prompt else 'Password'}: ")
                    if argument.prompt and not kwargs[argument.dest] and not argument.password:
                        kwargs[argument.dest] = input(f"{argument.prompt}: ")
                elif argument.nargs > 1:
                    '''Обрабатываем списки аргументов'''
                    for l in range(argument.nargs):
                        value = False if next_arg and next_arg[0:1] == '-' else next_arg
                        if value:
                            kwargs[argument.dest].append(value)
                        if argument.prompt and len(kwargs[argument.dest]) <= l:
                            kwargs[argument.dest].append(input(f"{argument.prompt}: "))
                        # arg = next_arg
                        if value:
                            '''Берем следующий только если текущий был найден, 
                            иначе будем получать пропуски элементов'''
                            next_arg = next(_args, False)
            arg = next_arg

        if argument.nargs > 1:
            if argument.required and argument.nargs != len(kwargs[argument.dest]):
                raise Exception(
                    f"Argument {argument.argument if argument.argument else argument.short} is required")
        elif argument.required and not kwargs[argument.dest]:
                raise Exception(
                    f"Argument {argument.argument if argument.argument else argument.short} is required")

    return kwargs


class DefaultThread(Thread):
    """
    Пример скачивание файла используя многопоточность
    """
    actions = ["active", "stop", "wait"]
    action = "active"

    def stop(self):
        self.action = 'stop'
        # raise StopThread(self.name)

    def wait(self):
        self.action = 'wait'
        # raise WaitThread(self.name)

    def active(self):
        self.action = 'active'

    def __init__(self, function=None):
        """Инициализация потока"""
        Thread.__init__(self)
        self.function = function
        self.name = function.__name__

    def run(self):
        if callable(self.function):
            self.function(self)
        # print(self.__dict__)


def daemon(*args, function=None, as_daemon=False, **kwargs):
    thread = threading.current_thread()
    if callable(function):
        function(thread)

    # print(thread.__dict__)
    # print(thread.daemon)
    # print(thread.isDaemon())
    # set thread as Daemon
    # thread.setDaemon(True)
    # print(thread.isDaemon())


class WaitThread(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        name -- name thread
        message -- explanation of the error
    """

    def __init__(self, name, message="Wait"):
        self.name = name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.name} -> {self.message}'


class StopThread(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        name -- name thread
        message -- explanation of the error
    """

    def __init__(self, name, message="Stop"):
        self.name = name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.name} -> {self.message}'


class ActiveThread(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        name -- name thread
        message -- explanation of the error
    """

    def __init__(self, name, message="Start"):
        self.name = name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.name} -> {self.message}'

