import os
from ..console import cli


@cli.group()
def localize(*args):
    """
    Группа команд локализации приложения. Так же если в системе не установлен gettext и pybabel, команда пытается
    его поставить. Для работы команд локализации должен быть настроен pybabel.

    """
    from ..core.popen import Popen
    from ..storage import StorageMapper

    storageMapper = StorageMapper()

    locale = storageMapper.get('locale')
    logger = storageMapper.get('logger')
    try:
        popen = Popen(['xgettext'])
        popen.execute(shutdown=True)
    except:
        try:
            logger.info(locale('Попытка установить gettext'))
            popen = Popen(['apt', 'install', 'gettext', '-y'])
            popen.execute(info=True)
        except:
            raise Exception(locale('Не удалось установить gettext. '
                                   'Перед использованием команды установить gettext вручную.'))

    try:
        popen = Popen(['pybabel'])
        popen.execute(shutdown=True)
    except:
        try:
            logger.info('Попытка установить pybabel')
            popen = Popen(['pip', 'install', 'pybabel', '-y'])
            popen.execute(info=True)
        except:
            try:
                logger.info(locale('Попытка установить pybabel'))
                popen = Popen(['pip3', 'install', 'pybabel', '-y'])
                popen.execute(info=True)
            except:
                raise Exception(locale('Не удалось установить gettext. '
                                       'Перед использованием команды установить pybabel вручную.'))


@localize.command(command_name='generate')
@localize.argument('--directory', short='-d', description='Директория локализаций')
@localize.argument('--domain', short='-D', description='Домен локализаций')
@localize.argument('--source', short='-s', description='Место поиска строк переводов', default='.')
def generate(*args, directory=None, domain=None, source=None):
    """
    Запускает генерацию файлов .pot. Команда проходит по файлам проекта, находит все подходящие строки и заносит в
    соответсвующие файлы. Для работы команды должен быть настроен pybabel.

    """
    from ..core.popen import Popen
    from ..storage import StorageMapper

    storageMapper = StorageMapper()

    locale = storageMapper.get('locale')
    logger = storageMapper.get('logger')
    config = locale.getConfig()
    if not directory:
        directory = config['directory']
    if not domain:
        domain = config['domain']
    logger.debug(locale("Генерация файла pot в дирректории {folder} из строк в функциях {translate_function}",
        folder = '',
        translate_function = ''
    ))
    try:
        pot_file = os.path.join(directory, '.'.join([domain, 'pot']))
        logger.debug(locale("Путь к файлу шаблона переводов pot: %s", pot_file))

        command = []
        command.append('pybabel')
        command.append('extract')
        command.append('--mapping-file=%s' % config['babelrc'])
        for tf in config['translate_functions']:
            command.append("--keywords=%s" % tf)
        command.append('--output-file={file}'.format(file=pot_file))
        command.append(source)

        popen = Popen(command)
        popen.execute(info=True)
        popen.toLogger()
        if not popen.getError():
            logger.info(locale("Файл шаблона переводов успешно создан %s", pot_file))
        else:
            raise Exception(popen.getError())
    except Exception as e:
        logger.exception(locale("Не удалось создать файл переводов"))


@localize.command(command_name='update')
def update(*args):
    """
    Запускает обновление файлов .po из файла pot. Команда проходит по файлам проекта, находит все подходящие
    строки и заносит в соответсвующие файлы. Для работы команды должен быть настроен pybabel.
    Перед использованием команды запустие `localize init`

    """
    from ..core.popen import Popen
    from ..storage import StorageMapper

    storageMapper = StorageMapper()

    locale = storageMapper.get('locale')
    logger = storageMapper.get('logger')
    config = locale.getConfig()
    try:
        pot_file = os.path.join(config['directory'], '.'.join([config['domain'], 'pot']))

        logger.debug(locale("Генерация файла po в дирректории {folder} из файла {pot_file}",
            folder=config['directory'],
            pot_file=pot_file
        ))

        for lang in config['languages']:

            po_file = os.path.join(config['directory'], lang, 'LC_MESSAGES', '.'.join([config['domain'], 'po']))

            logger.debug(locale("Путь файл переводов {po_file}",
                lang=lang,
                pot_file=pot_file,
                po_file=po_file
            ))

            command = []
            command.append('pybabel')
            if os.path.exists(po_file):
                command.append('update')
            else:
                command.append('init')
            command.append('--domain={domain}'.format(domain=config['domain']))
            command.append('--input-file={file}'.format(file=pot_file))
            # command.append('--output-dir={directory}'.format(directory=config['directory']))
            command.append('--output-file={po_file}'.format(po_file=po_file))
            command.append('--locale={locale}'.format(locale=lang))

            popen = Popen(command)
            popen.execute(info=True)
            popen.toLogger()

            if not popen.getError():
                logger.info(locale("Файл перевода успешно создан: %s", po_file))
            else:
                raise Exception(popen.getError())
    except Exception as e:
        logger.exception(locale("Не удалось создать файл переводов"))


@localize.command(command_name='compile')
def compile(*args):
    """
    Запускает компилцию файлов .po в файлы .mo. Для работы команды должен быть настроен pybabel.
    Перед использованием команды запустие `localize init` или `localize update` что бы сгенерировать po файлы.

    """
    from ..core.popen import Popen
    from ..storage import StorageMapper

    storageMapper = StorageMapper()

    locale = storageMapper.get('locale')
    logger = storageMapper.get('logger')
    config = locale.getConfig()
    for lang in config['languages']:
        # for po_file in sorted(glob.glob(os.path.join(directory, '**', '*.po'), recursive=True)):
        try:
            command = []
            command.append('pybabel')
            command.append('compile')
            command.append('--domain={domain}'.format(domain=config['domain']))
            # command.append('--input-file={file}'.format(file=po_file))
            # command.append('--output-file={file}'.format(file=config['directory']))
            command.append('--directory={directory}'.format(directory=config['directory']))
            command.append('--locale={locale}'.format(locale=lang))

            popen = Popen(command)
            popen.execute()
            popen.toLogger()

            logger.info(popen.getResult())

            if not popen.getError():
                logger.info(locale("Файлы переводов скомпилированы в директории %s", config['directory']))
            else:
                raise Exception(popen.getError())
        except Exception as e:
            logger.exception(locale("Не удалось скомпилировать файл переводов"))

