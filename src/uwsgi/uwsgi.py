from ..storage import StorageMapper
storageMapper = StorageMapper()


class UwsgiReload:
    """
    Команда перезагрузки UWSGI
    """

    def __init__(self, config={}):
        self.config = config

    def execute(self):
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')

        logger.info(locale('Код приложения изменен: Перезапускаем приложение'))
        import uwsgi
        return uwsgi.reload()
