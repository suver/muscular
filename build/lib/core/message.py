import sys
from ..console import Colors

def message(text, params={}, lang=None):
    """
    Функция возвращает форматированную строку сообщения

    :param text:
    :param params:
    :param lang:
    :return:
    """
    return text.format(**params)


def alert(text, params={}, lang=None, message_type=None):
    """
    Функция выводит сообщение с предупреждением

    :param message_type:
    :param text:
    :param params:
    :param lang:
    :return:
    """
    if sys.stdout.isatty():
        if message_type == 'warning':
            print(Colors.WARNING, message(text, params=params, lang=lang), Colors.ENDC)
        else:
            print(message(text, params=params, lang=lang))
    else:
        return message(text, params=params, lang=lang)