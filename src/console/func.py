from __future__ import annotations
import threading
import getpass


def argsparse(arguments, args):
    """
    @TODO переписать логику
    Парсер аргументов командной строки

    :param arguments:
    :param args:
    :return:
    """
    kwargs = {}
    new_args = list(args)
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
                if arg in new_args:
                    new_args.remove(arg)
                if argument.nargs <= 0:
                    '''Обрабатываем флаги'''
                    kwargs[argument.dest] = argument.flag_value
                elif argument.nargs == 1:
                    '''Обрабатываем элемент со значением'''
                    value = False if next_arg and next_arg[0:1] == '-' else next_arg
                    if value:
                        if value in new_args:
                            new_args.remove(value)
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
                            if value in new_args:
                                new_args.remove(value)
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

    return tuple(new_args), kwargs


def daemon(*args, function=None, as_daemon=False, **kwargs):
    """
    Создает процесс демона

    :param args:
    :param function: Функция для запуска в качестве демона
    :param as_daemon: запускает как демон. Т.е. ждем когда функция закончит выполнения перед остановкой демона
    :param kwargs:
    :return:
    """
    thread = threading.current_thread()
    if callable(function):
        function(thread)

    # print(thread.__dict__)
    # print(thread.daemon)
    # print(thread.isDaemon())
    # set thread as Daemon
    # thread.setDaemon(True)
    # print(thread.isDaemon())