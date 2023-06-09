import subprocess
import typing
from ..storage import StorageMapper
storageMapper = StorageMapper()


class Popen:
    """
    Process Open
    Класс позволяет выполнять команду в обочке bash операционной системе.

    command = ['ping', 'localhost']
    -- or --
    command = 'ping localhost'

    popen = Popen(command)
    popen.execute()


    popen.getResult() - получаем результат выполненния команды.
    popen.getError() - получаем ошибки, если есть
    popen.toLogger() - заносим всю информацию через системные логеры

    """

    def __init__(self, command: typing.Union[str,list]):
        """
        Создаем объект команды

        :param command: выполняемая команда
        """
        if isinstance(command, list):
            self.command = command
        elif  isinstance(command, str):
            self.command = command.split(' ', command)
        else:
            raise Exception('`command` может быть строкой или списком')
        self.result = None
        self.error = None

    def execute(self, info=True, shutdown=False) -> bool:
        """
        Выполняет установленную команду в среде операционной системы

        :return:
        """
        logger = storageMapper.get('logger')
        locale = storageMapper.get('locale')
        try:
            if not shutdown:
                if not info:
                    logger.debug(locale("Запуск: %s", ' '.join(self.command)))
                else:
                    logger.info(locale("Запуск: %s", ' '.join(self.command)))
            process = subprocess.run(self.command,
                                     universal_newlines=True,
                                     shell=False,
                                     check=True,
                                     capture_output=True
                               )
            self.result = process.stdout + process.stderr
            return True
        except subprocess.CalledProcessError as err:
            self.error = err.stderr
            return False

    def getResult(self) -> typing.Union[str, None]:
        """
        Возвращает результат работы команды в виде строки или None

        :return: Union[str, None]
        """
        if self.result:
            return self.result

    def getError(self) -> typing.Union[str, None]:
        """
        Возвращает ошибки в результате работы команды в виде строки или None

        :return: Union[str, None]
        """
        if self.error:
            return self.error

    def toLogger(self) -> None:
        """
        Заносит информацию о результате или ошибке через системный логер

        :return: None
        """
        logger = storageMapper.get('logger')
        locale = storageMapper.get('locale')
        if self.result:
            logger.debug(locale("Команда вернула: %s", self.result))
        if self.error:
            logger.warning(locale("Команда вернула ошибку: %s", self.error))