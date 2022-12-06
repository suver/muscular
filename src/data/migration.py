import os
from ..console import cli
import importlib.machinery
import importlib.util
from .database import DBPool
from .drivers import Postgres
from ..models import Collection, Column, String
from ..storage import StorageMapper
storageMapper = StorageMapper()
locale = storageMapper.get('locale')
logger = storageMapper.get('logger')


def is_checkpoint(connection, file):
    """
    Проверяем есть ли запись о том что файл миграции уже был обработан ранее

    :param connection:
    :param file:
    :return:
    """

    rows = connection.execute(
        'SELECT * '
        'FROM migrations '
        'WHERE migrate=:file '
        'LIMIT 1', {
            "file": file
        })
    if rows and rows.rowcount > 0:
        return True
    return False


def save_checkpoint(connection, file):
    """
    Сохраняет информацию о том что файл был обработан

    :param connection:
    :param file:
    :return:
    """
    connection.execute(
        'INSERT INTO migrations (migrate) VALUES (:file)', {
            "file": file
        })


def remove_checkpoint(connection, file):
    """
    Удаляет запись о том что файл был обработан.

    :param connection:
    :param file:
    :return:
    """
    connection.execute(
        'DELETE FROM migrations WHERE migrate=:file', {
            "file": file
        })


t = Collection('migrations',
    Column('migrate', String),
)

@cli.group(description=locale('Группа команд для работы с миграциями'))
def migrate(*args):
    """
    Команды для работы с миграциями. Этой командой создается структура БД с миграциями в мета базе если
    ранее такой коллекции не было создано.

    """
    pool = DBPool(Postgres)
    for connection_name, connect in pool:
        if connect.meta:
            if not connect.is_collection('migrations'):
                logger.debug(locale('Создаем коллекцию `migrations`'))
                connect.transaction()
                connect.collection(t).create()
                connect.commit()
        else:
            logger.exception(locale('Необходимо для одного из соеденений с типом Postgres установить флаг '
                                    '`meta` рвным True'))



@migrate.command(command_name='up', description=locale('Применить миграцию'))
def up(*args):
    """
    migrate up проверяет прпау с миграциями и применяет те, что еще не были применены ранее
    """
    path='./migrations'

    meta_connect = None
    pool = DBPool(Postgres)
    for connection_name, connect in pool:
        if connect.meta:
            meta_connect = connect

    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():

                # Import module
                loader = importlib.machinery.SourceFileLoader('module', '/'.join([path, entry.name]))
                spec = importlib.util.spec_from_loader('module', loader)
                module = importlib.util.module_from_spec(spec)
                loader.exec_module(module)
                if not is_checkpoint(meta_connect, entry.name):
                    logger.info(locale("Запуск: %s", entry.name))
                    if module.up():
                        save_checkpoint(meta_connect, entry.name)
                    else:
                        logger.error(locale('Прервали выполнение. Миграция не вернула True, вероятно во '
                              'время выполнения возникли ошибки.'))
                        break


@migrate.command(command_name='down', description=locale('Откатить миграцию'))
@migrate.argument('--limit', short='-l', description=locale('Колличество миграций для отката'),
                  prompt=locale('Введите число миграций для отката'), default=1)
def down(*args, limit=1):
    """
    migrate down читает журнал миграций и откатывает крайнюю
    migrate down --limit 2 откатит последние две миграции
    """
    path='./migrations'

    meta_connect = None
    pool = DBPool(Postgres)
    for connection_name, connect in pool:
        if connect.meta:
            meta_connect = connect

    rows = meta_connect.execute(
        'SELECT * FROM migrations ORDER BY migrate DESC LIMIT :limit', {
            "limit": int(limit)
        })
    if rows and rows.rowcount > 0:
        for row in rows:
            logger.info("Запуск: %s", os.path.join([path, row.migrate]))
            loader = importlib.machinery.SourceFileLoader('module', '/'.join([path, row.migrate]))
            spec = importlib.util.spec_from_loader('module', loader)
            module = importlib.util.module_from_spec(spec)
            loader.exec_module(module)

            if module.down():
                remove_checkpoint(meta_connect, row.migrate)
            else:
                logger.error(locale('Прервали выполнение. Миграция не вернула True, вероятно во '
                      'время выполнения возникли ошибки.'))
                break

