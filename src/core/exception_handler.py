import sys
from ..storage import StorageMapper
storageMapper = StorageMapper()


class ExceptionHandler:

    def __init__(self):
        def muscular_excepthook(exctype, value, traceback):
            locale = storageMapper.get('locale')
            logger = storageMapper.get('logger')
            if exctype == KeyboardInterrupt:
                logger.info(locale('Прерываем процесс по требованию'))
                exit()
            else:
                logger.exception(value)
                sys.__excepthook__(exctype, value, traceback)
                exit()
        sys.excepthook = muscular_excepthook