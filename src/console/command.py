from __future__ import annotations
import typing
from pprint import pprint
from typing import List
from functools import wraps
from typing import Dict
import os
from .colory import Colors
from .func import argsparse
from ..core.cli import CliCommand
from ..storage import StorageMapper

storageMapper = StorageMapper()
logger = storageMapper.get('logger')
locale = storageMapper.get('locale')


def print_help(instance):
    """
    Выводит подсказу в качестве результата работы команды

    :param instance:
    :return:
    """
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
    except:
        rows = 50
        columns = 100

    def split_str(string, length):
        if len(string) <= length:
            yield string
        else:
            for i in range(0, len(string), length):
                yield string[i:i + length].strip()


    print(f"\n")
    print(f"{Colors.WARNING}", locale("help - список доступных команд"), f"{Colors.ENDC}")
    print(f"{Colors.WARNING}", locale("help <command> - помощь по команде"), f"{Colors.ENDC}")
    print("\n")

    if hasattr(instance, '_children'):
        for command in instance._children:
            if command.description:
                for (i, string) in enumerate(split_str(' '.join(command.description.split()), int(columns) - 23)):
                    if i == 0:
                        print("{command} - {description}".format(command=command.command_name.ljust(20), description=string))
                    else:
                        print(' ' * 22, string.ljust(int(columns) - 23))
            if isinstance(command, Command):
                for i, argument in enumerate(command.arguments):
                    arg = "{s1}{s2}{s3}{s4}{s5}".format(
                        s1='[' if argument.required else '',
                        s2=argument.argument,
                        s3=', ' if argument.short else '',
                        s4=argument.short if argument.short else '',
                        s5=']' if argument.required else ''
                    )
                    print(
                        " ".ljust(1),
                        arg.ljust(20),
                        argument.description.ljust(80)
                    )
    else:
        print("{command}\n\n{description}".format(
            command=instance.command_name.ljust(20),
            description=instance.handler.__doc__ if instance.handler.__doc__ else locale('<Описание отсутсвует>')))

    print(f"\n")
    return True


class Command(CliCommand):
    """
    Класс для обработки консольных команд

    """

    def __init__(self, key: typing.Optional[str|list],
                 function_name: typing.Optional[str] = None,
                 handler: typing.Optional[callable] = None,
                 description: str = '',
                 command_name: typing.Optional[str] = None):
        """
        Конструктор консольной команды

        :param key: идентификатор консольной команды
        :param function_name:
        :param handler: Обработчик консольной команды
        :param description: Текстовое описание команды
        :param command_name: название консольной команды
        """
        if not key:
            raise Exception(locale('`key` не указан'))
        self._key = key
        self._function_name = function_name
        self._handler = handler
        self._description = description
        self._parent = None
        self._command_name = command_name if command_name else '-'.join(key)
        self._arguments = []

    def __repr__(self):
        return "Command(%s)" % ', '.join([
            'key=%s' % '/'.join(self.key),
            'function_name=%s' % self.function_name,
            'handler=%s' % "{}.{}".format(str(self.handler.__module__), str(self.handler.__name__)),
            'command_name=%s' % self.command_name,
        ])

    @property
    def function_name(self) -> str:
        return self._function_name

    @function_name.setter
    def function_name(self, function_name) -> None:
        self._function_name = function_name

    @property
    def handler(self) -> callable:
        return self._handler

    @handler.setter
    def handler(self, handler):
        self._handler = handler

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description) -> None:
        self._description = description

    @property
    def command_name(self) -> str:
        return self._command_name

    @command_name.setter
    def command_name(self, command_name) -> None:
        self._command_name = command_name

    @property
    def arguments(self) -> List:
        return self._arguments

    @arguments.setter
    def arguments(self, arguments) -> None:
        self._arguments = arguments

    def add_argument(self, argument: Argument) -> None:
        """
        Добавляет аргемент к консольной команде

        :param argument: объект класса Argument
        :return:
        """
        self._arguments.append(argument)

    def add_arguments(self, arguments: list[Argument]) -> None:
        """
        Добавляет список аргументов к консольной команде

        :param arguments: список объектов класса Argument
        :return:
        """
        for argument in arguments:
            self._arguments.append(argument)

    def execute(self, *args, **_kwargs):
        """
        Запускает обработку консольной команды

        """
        if hasattr(self.handler, 'arguments'):
            arguments = self.handler.arguments
        else:
            arguments = []
        args, kwargs = argsparse(arguments, args)
        kwargs.update(_kwargs)
        params = {}
        if hasattr(self.handler, 'arguments'):
            for argument in self.handler.arguments:
                params.update({argument.dest: kwargs.get(argument.dest, argument.default)})
        result = self.handler(*args, **params)
        return result


class Argument:
    """
    Клас обраотки декоратов для установки возможных значений к консольным командам

    """

    _dest = None
    _argument = None
    _short = None
    _required = False
    _description = ''
    _default = False
    _multiple = False
    _flag_value = True
    _nargs = 0
    _prompt = None
    _value = None
    _password = None

    def __init__(self,
                 argument: typing.Optional[str] = None,
                 short: typing.Optional[str] = None,
                 dest: typing.Optional[str] = None,
                 required: bool = False,
                 description: str = '',
                 default: bool = False,
                 multiple: bool = False,
                 flag_value: bool = True,
                 nargs: int = 0,
                 prompt: typing.Optional[str] = None,
                 password: typing.Optional[str] = None
             ):
        """
        Контструктор объекта аргумента

        :param argument: строка параметр аргумента для консольной команды
        :param short: краткий параметр аргумента консольной команды
        :param dest: название аргумента, которому будет передо значение аргумента из консольной команды
        :param required: Истина, если аргумент обязательный
        :param description: Описание аргумента
        :param default: Значение по умолчанию
        :param multiple: Если Истина то рагемнт можно указать несколько раз в одной консольной команде
        :param flag_value: Если Истина то наличие аргумента устанавливает параметр в Истину, а отсутвсие означает Лож
        :param nargs: Колличество значений аргумента
        :param prompt: Если указан, то в консоли при выполнении команды будет задан вопрос с текстом из параметра и
                        команда примет введенный пользователем аргумент в качестве значения
        :param password: Установите если значение аргумента должно быть скрыто
        """
        self.dest = dest
        self.argument = argument
        self.short = short
        self.required = required
        self.description = description
        self.default = default
        self.value = default
        self.multiple = multiple
        self.flag_value = flag_value
        self.nargs = nargs
        self.prompt = prompt
        self.password = password

    def __repr__(self):
        return "Argument(%s)" % ', '.join([
            'argument=%s' % self.argument,
            'short=%s' % self.short,
            'dest=%s' % self.dest,
            'required=%s' % self.required,
            'default=%s' % self.default,
            'multiple=%s' % self.multiple,
            'flag_value=%s' % self.flag_value,
            'nargs=%s' % self.nargs,
            # 'prompt=%s' % self.prompt,
            'password=%s' % self.password,
        ])

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value

    @property
    def dest(self) -> str:
        return self._dest

    @dest.setter
    def dest(self, dest) -> None:
        if dest:
            self._dest = dest

    @property
    def argument(self) -> str:
        return self._argument

    @argument.setter
    def argument(self, argument: str) -> None:
        if not argument:
            return
        if argument[0:2] == '--':
            dest = argument[2:]
        elif argument[0:1] == '-':
            dest = argument[1:]
        else:
            raise Exception(locale("Аргумент `%s` должен начинаться с -- или -", argument))
        self.dest = dest
        self._argument = argument

    @property
    def short(self) -> str:
        return self._short

    @short.setter
    def short(self, short: str) -> None:
        self._short = short

    @property
    def prompt(self) -> str:
        return self._prompt

    @prompt.setter
    def prompt(self, prompt: str) -> None:
        if prompt and self._nargs <= 0:
            self._nargs = 1
        self._prompt = prompt

    @property
    def required(self) -> bool:
        return self._required

    @required.setter
    def required(self, required: bool) -> None:
        self._required = required

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description) -> None:
        self._description = description

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, default) -> None:
        self._default = default

    @property
    def multiple(self) -> bool:
        return self._multiple

    @multiple.setter
    def multiple(self, multiple: bool) -> None:
        self._multiple = multiple

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password) -> None:
        if password:
            self.nargs = 1
        self._password = password

    @property
    def flag_value(self):
        return self._flag_value

    @flag_value.setter
    def flag_value(self, flag_value) -> None:
        self._flag_value = flag_value

    @property
    def nargs(self) -> int:
        return self._nargs

    @nargs.setter
    def nargs(self, nargs: int) -> None:
        self._nargs = nargs


class Group(CliCommand):
    """
    Класс для работы с группами консольных команд

    """

    _commands: Dict[str] = {}

    def __init__(self,
                 key: typing.Optional[str|list] = None,
                 function_name: str = None,
                 handler: callable = None,
                 description: str = '',
                 command_name: typing.Optional[str] = None
             ):
        """
        Конструктор объекта группы

        :param key: идентификатор группы
        :param function_name:
        :param handler: обрбаотчик группы
        :param description: описнаие группы
        :param command_name: название команды группы
        """
        self._children: List[(Command, Group)] = []
        self._key = key
        self._function_name = function_name
        self._handler = handler
        self._description = description
        self._parent = None
        self._command_name = command_name if command_name else '-'.join(key)
        self._arguments = []

    def __repr__(self):
        return "Group(%s)" % ', '.join([
            'key=%s' % '/'.join(self.key),
            'function_name=%s' % self.function_name,
            'handler=%s' % "{}.{}".format(str(self.handler.__module__), str(self.handler.__name__)),
            'command_name=%s' % self.command_name,
            'arguments=%s' % self.arguments,
            'arguments=%s' % self.handler.arguments if hasattr(self.handler, 'arguments') else '[]',
        ])

    @property
    def function_name(self) -> str:
        return self._function_name

    @function_name.setter
    def function_name(self, function_name) -> None:
        self._function_name = function_name

    @property
    def handler(self) -> object:
        return self._handler

    @handler.setter
    def handler(self, handler):
        self._handler = handler

    @property
    def arguments(self) -> List:
        return self._arguments

    @arguments.setter
    def arguments(self, arguments) -> None:
        self._arguments = arguments

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description) -> None:
        self._description = description

    @property
    def command_name(self) -> str:
        return self._command_name

    @command_name.setter
    def command_name(self, command_name) -> None:
        self._command_name = command_name

    def add(self, command: (Command, Group)) -> None:
        """
        Добавляет к группе новую команду или другую группу

        :param command: объект группы или команды
        :return:
        """
        self._children.append(command)
        command.parent = self

    def remove(self, command: (Command, Group)) -> None:
        """
        Удаляет из группы команду или другую группу

        :param command: объект группы или команды
        :return:
        """
        self._children.remove(command.key)
        command.parent = None

    def execute(self, *args, **_kwargs):
        """
        Запускает выполнение обработчика группы

        :param args:
        :param _kwargs:
        :return:
        """
        if hasattr(self.handler, 'arguments'):
            arguments = self.handler.arguments
        else:
            arguments = []
        if isinstance(args, str):
            args = [args]
        args, kwargs = argsparse(arguments, args)
        kwargs.update(_kwargs)
        params = {}
        if hasattr(self.handler, 'arguments'):
            for argument in self.handler.arguments:
                params.update({argument.dest: kwargs.get(argument.dest, argument.default)})
        result = self.handler(*args, **params)
        if len(args) >= 1:
            for command in self._children:
                if len(args[0:1]) > 0 and command.command_name == args[0:1][0]:
                    return command.execute(*args[1:], **kwargs)
            print(f"\n")

            if len(args[0]) > 0:
                logger.warning(locale("Команда `{arg}` не найдена", args[0]))
        return result

    def help(self, *args, **kwargs):
        """
        Устанавливает команду вывода помощи для подсказок по группе

        :param args:
        :param kwargs:
        :return:
        """
        self._help(args[:-1], self)

    def _help(self, args, command):
        if len(args) > 0:
            args, _command = args[1:] if len(args[1:]) > 0  else [], args[0:1][0] if len(args[0:1]) > 0 else None
            if hasattr(command, '_children') and len(command._children) > 0:
                for c in command._children:
                    if c.command_name == _command:
                        self._help(args, c)
        else:
            return print_help(command)

    def _default_func_prop(self, func):
        if not hasattr(func, 'arguments'):
            setattr(func, 'arguments', [])
        if not hasattr(func, 'command'):
            setattr(func, 'command', None)
        if not hasattr(func, 'group'):
            setattr(func, 'group', None)

    def command(self, command_name=None, description=None):
        """
        Декоратор устанавливающий функцию как обработчик команды

        :param command_name: название команды
        :return:
        """
        def decorator(func):
            self._default_func_prop(func)
            key = [func.__name__] + self.key
            _command = Command(key)
            _command.command_name = command_name if command_name else func.__name__
            _command.description = description if description is not None else func.__doc__
            _command.function_name = func.__name__
            _command.handler = func
            _command.add_arguments(func.arguments)
            self.add(_command)
            # _command = commandFactory.update(key, _command)
            setattr(func, 'command', _command)

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            return wrapper

        return decorator

    def group(self, description=None, command_name=None):
        """
        Декоратор устанавливающий функцию как обработчик группы команд

        :param description: описнаие
        :param command_name: название команды
        :return:
        """
        def decorator(func):
            self._default_func_prop(func)
            key = [func.__name__] + self.key
            _group = Group(key)
            _group.command_name = command_name if command_name else func.__name__
            _group.function_name = func.__name__
            _group.description = description if description is not None else func.__doc__
            _group.handler = func
            setattr(func, 'group', _group)
            self.add(_group)

            # key = ['help'] + _group.key
            # _command = Command(key)
            # _command.function_name = _group.help.__name__
            # _command.handler = _group.help
            # _command.command_name = 'help'
            # _command.description = locale("список команд")

            # _group.add(_command)

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            return _group

        return decorator

    def argument(self, argument, short=None, description='', required=False, default=False,
                 multiple=False, flag_value=True, dest=None, nargs=0, prompt=None, password=False):
        """
        Декоратор устанавливающий к функции определенной декоратором группы или команды новые аргументы

        :param argument: строка параметр аргумента для консольной команды
        :param short: краткий параметр аргумента консольной команды
        :param dest: название аргумента, которому будет передо значение аргумента из консольной команды
        :param required: Истина, если аргумент обязательный
        :param description: Описание аргумента
        :param default: Значение по умолчанию
        :param multiple: Если Истина то рагемнт можно указать несколько раз в одной консольной команде
        :param flag_value: Если Истина то наличие аргумента устанавливает параметр в Истину, а отсутвсие означает Лож
        :param nargs: Колличество значений аргумента
        :param prompt: Если указан, то в консоли при выполнении команды будет задан вопрос с текстом из параметра и
                        команда примет введенный пользователем аргумент в качестве значения
        :param password: Установите если значение аргумента должно быть скрыто
        :return:
        """
        def decorator(func):
            self._default_func_prop(func)
            _argument = Argument()
            _argument.argument = argument
            _argument.short = short
            _argument.description = description
            _argument.required = required
            _argument.default = default
            _argument.multiple = multiple
            _argument.dest = dest
            _argument.flag_value = flag_value
            _argument.nargs = nargs
            _argument.prompt = prompt
            _argument.password = password
            func.arguments.append(_argument)
            func.arguments.append(_argument)
            self.arguments = getattr(func, 'arguments')

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            return wrapper

        return decorator

    def flag(self, argument, short=None, description='', dest=None, default=False, flag_value=True):
        """
        Декоратор устанавливающий к функции определенной как декоратором группы или команды новый лаг

        :param argument: строка параметр аргумента для консольной команды
        :param short: краткий параметр аргумента консольной команды
        :param dest: название аргумента, которому будет передо значение аргумента из консольной команды
        :param description: Описание аргумента
        :param default: Значение по умолчанию
        :param flag_value: Если Истина то наличие аргумента устанавливает параметр в Истину, а отсутвсие означает Лож
        :return:
        """
        def decorator(func):
            self._default_func_prop(func)
            _argument = Argument()
            _argument.argument = argument
            _argument.short = short
            _argument.description = description
            _argument.required = False
            _argument.default = default
            _argument.multiple = False
            _argument.dest = dest
            _argument.flag_value = flag_value
            _argument.nargs = 0
            _argument.prompt = None
            func.arguments.append(_argument)
            self.arguments = func.arguments

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            return wrapper

        return decorator

