import gettext
import os
import typing
from ..configuration import Configurator
from ..storage import StorageMapper

storageMapper = StorageMapper()


class Language(object):
    """
    Класс для создания объекта языка. Реализован с патерном Одиночка, а это значит что любой вызов этого класса
    приведет к передаче в переменную одного и того же экземпляра объекта.

    ВНИМАНИЕ: Данный объект не стоит использовать для установки языка, так как это вспомогательный класс для
    хранения общего языка системы, но не для установки языка. Вместо этого используйте
    Locale.setLanguage('ru', name='default')

    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Реализация патерна одиночка

        :param args:
        :param kwargs:
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Конструктор объекта языка

        """
        if not hasattr(self, '_language'):
            self._language = None

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        self._language = value

    @staticmethod
    def set(value):
        """
        Устанавливает язык

        :param value: код языка
        :return:
        """
        lang = Language()
        lang._language = value

    @staticmethod
    def get():
        """
        Возвращает код языка

        :return:
        """
        lang = Language()
        return lang._language

    @staticmethod
    def isInstall():
        """
        Проверяет установлен ли язык в область храненрия

        :return:
        """
        lang = Language()
        return lang.language is not None


class Locale(object):
    """
    Класс локализации приложения. С помощью данного класса проводиться настройка и получения объекта gettext,
    который учавствует в локализации приложения.

    Настройка проводиться либо через файл конфигурации:
    locale:
      domain: muscular
      languages: [en]
      search_mask:
        - "**/*.py"
      locales_dir: !basepath locales
      fallback: False

    config = Configurator(file=config_file)
    locale = Locale(config=config.get('locale'), install=True)


    Либо через параметры объекта


    config = Configurator(file=config_file)
    locale = Locale(
        config=config.get('locale'),    - объект Configuration. Имеет приемущество перед остальными опциями.
        install=True,                   - если Истина то производится установка глобального объекта "_"
        domain='messages',              - домен перевода
        languages=[],                   - список языков используемых в системе
        search_mask=["**/*.py"],        - маска поиска файла для выполнения команд localize
        locales_dir='locales',          - директория с файлами перевода
        fallback=True                   - если Истина, выдает ошибку если перевода строки нет
    )


    locale.switch('ru')
    -- or --
    Locale.setLanguage('ru', name='default')

    """

    _instances = dict()

    def __new__(cls, *args, name: str = 'default', **kwargs):
        """
        Реализация патерна одиночка

        :param args:
        :param kwargs:
        """
        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
        return cls._instances[name]

    def __call__(self, *args, **kwargs) -> str:
        """
        Переводит строку на выбранный язык

        :param message: строка для перевода
        :return: str переведенная строка
        """
        logger = storageMapper.get('logger')
        if len(args) > 0:
            message = args[0]
        else:
            raise Exception(logger('Не передана строка для перевода'))
        return str(self.t(message, *args, **kwargs))

    def __init__(self,
                 name: str = 'default',
                 config: typing.Optional[Configurator] = None,
                 install: bool = False,
                 domain: str = 'messages',
                 languages=None,
                 directory: str = 'locales',
                 fallback: bool = True,
                 translate_functions: typing.Optional[list] = None,
                 babelrc: typing.Optional[str] = None,
                 default_language: typing.Optional[str] = None,
                 ):
        """
        Конструктор класса Locale
        Устанвливаем конфигурацию языка и файлов перевода

        :param name: назваие инстанса для разделения конфигураций языка
        :param config: Объект класса Configurator. По умолчанию None
        :param install: Если Истина то устанвливаем глобальные переменные для перевода строк. По умолчанию False
        :param domain: Домен перевода (файл с переводом)
        :param languages: Допустимые языки переводов. По умолчанию ['ru']
        :param directory: Директория хранения локализаций. По умолчанию locales
        :param fallback: Ошибка если перевода нет. По умолчанию True
        :param default_language: Язык по умолчанию, системный язык
        """
        if babelrc is None:
            babelrc = 'babelrc'
        if languages is None:
            languages = ['ru']

        first_run = False
        if not hasattr(self, '_config'):
            first_run = True
            self._config = dict()
            self._config['install'] = install
            self._config['install_language'] = None
            self._config['translate_functions'] = None
            self._config['name'] = name
            self._config['install_language'] = None

        if first_run:
            if config is not None:
                self._config['domain'] = config.get('domain', default=domain).value()
                self._config['babelrc'] = config.get('babelrc', default=babelrc).value()
                self._config['directory'] = config.get('directory', default=directory).value()
                self._config['languages'] = config.get('languages', default=languages).value()
                self._config['fallback'] = config.get('fallback', default=fallback).value()
                self._config['default_language'] = config.get('default_language', default=default_language).value()
                self._config['codeset'] = config.get('codeset', default=['unspecified']).value()
                self._config['translate_functions'] = config.get('translate_functions',
                                                                 default=translate_functions).value()
            else:
                self._config['domain'] = domain
                self._config['directory'] = directory
                self._config['languages'] = languages
                self._config['default_language'] = default_language
                self._config['fallback'] = fallback
                self._config['babelrc'] = babelrc
                self._config['translate_functions'] = translate_functions
                self._config['codeset'] = ['unspecified']

        if not Language.isInstall():
            self.switch(self._config['default_language'])

        if not Language.isInstall():
            for envar in ('LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG'):
                val = os.environ.get(envar)
                if val:
                    lang, = val.split(':')
                    self.switch(lang)
                    break

        self._setLocale()

    def switch(self, language: str = None):
        """
        Переключает язык на один из языков перевода. Если язык найти не удалось переключает на язык по умолчанию

        :param language: язык системы
        :return:
        """
        if not language or language not in self._config['languages']:
            if not Language.isInstall():
                Language.set(self._config['default_language'])
        else:
            Language.set(language)
        self._setLocale()

    def _setLocale(self):
        logger = storageMapper.get('logger')
        try:
            for _instance in self._instances:
                instance = self._instances[_instance]
                if instance._config['install_language'] is not Language.get():
                    instance._gettext = gettext.translation(instance._config['domain'],
                                                            localedir=instance._config['directory'],
                                                            languages=[Language.get()],
                                                            fallback=instance._config['fallback'],
                                                            codeset=instance._config['codeset']
                                                            )

                    instance._config['install_language'] = Language.get()

                    if instance._config['install']:
                        # self._gettext.install()
                        import builtins
                        builtins.__dict__['_'] = instance.t
                        # allowed = {'gettext', 'lgettext', 'lngettext',
                        #            'ngettext', 'npgettext', 'pgettext'}
                        # for name in allowed:
                        #     builtins.__dict__[name] = getattr(self._gettext, name)
                    #
                    logger.debug(instance.t('Устанавливаем язык на {lang} в экземпляре {instance}',
                                            lang=Language.get(),
                                            instance=_instance))
        except Exception as e:

            logger.exception(e)

    @staticmethod
    def getInstance(name: str = 'default'):
        """
        Получаем инстанс объекта Locale

        locale = Locale.getInstance()

        :param name: назваие инстанса для разделения конфигураций языка
        :return: Locale
        """
        return Locale(name=name)

    @staticmethod
    def setLanguage(language: str = None, name: str = 'default'):
        """
        Переключает язык на один из языков перевода. Если язык найти не удалось переключает на язык по умолчанию

        Locale.setLanguage('ru')

        :param name: назваие инстанса для разделения конфигураций языка
        :param language: язык
        :return:
        """
        locale = Locale.getInstance(name=name)
        locale.switch(language)

    def getConfig(self) -> typing.Dict:
        """
        Возвращает найстроки конфигурации

        :return:
        """
        return self._config

    def t(self, message: str, *args, **kwargs) -> str:
        """
        Переводит строку на выбранный язык

        :param message: строка для перевода
        :return: str переведенная строка
        """
        if hasattr(self, '_gettext'):
            if len(args[1:]) > 0:
                return self._gettext.gettext(message).format(**kwargs) % args[1:]
            else:
                return self._gettext.gettext(message).format(**kwargs)
        else:
            return message.format(**kwargs) % args[1:]
