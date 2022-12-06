from ...schema import Model, Key
from ...schema import Collection, Column
from sqlalchemy import create_engine, text
from ..driver import DatabaseLinkDriver, DataDriver
from ...storage import StorageMapper
storageMapper = StorageMapper()


class LinkDatabaseLinkDriver(DatabaseLinkDriver):
    """
    Link объект для подключения к БД
    """

    def connect(self, config=None) -> DataDriver:
        """
        Инициируем подключение к базе данных.

        :param config: Параметры соединения.
        :return: DataDriver
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if config is None:
            config = {}
        url = "{driver}://{user}:{password}@{host}:{port}/{database}".format(
            driver=config.driver,
            host=config.host,
            port=config.port,
            user=config.user,
            password=config.password,
            database=config.database,
        )
        logger.debug(locale("Подключаемся {driver_name}.connect({url})",
            driver_name=self.instance.__class__.__name__,
            url=url
        ))
        self.instance.url = url
        self.instance.engine = create_engine(url, future=True)
        self.instance.connection = self.instance.engine.connect()
        return self.instance

    def get_url(self):
        return self.instance.url


class ExecuteDatabaseLinkDriver(DatabaseLinkDriver):
    """
    Link объект для подключения к БД
    """

    def execute(self, query, params=None):
        """
        Выполняем запрос к базе данных

        :param query:
        :param params:
        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if not self.instance.connection:
            return None
        logger.debug(locale('{driver_name}.execute("{query}", {params})',
            query=query,
            params=params,
            driver_name=self.instance.__class__.__name__
        ))
        result = self.instance.connection.execute(text(query), params)
        if not self.instance._session:
            self.instance.commit()
        return result


class TransactionDatabaseLinkDriver(DatabaseLinkDriver):
    """
    Link объект для подключения к БД
    """

    def __init__(self, instance):
        super().__init__(instance)
        if not hasattr(self.instance, '_session'):
            self.instance._session = False

    def transaction(self):
        """
        Включаем механизм транзакций

        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if not self.instance.connection:
            return None
        self.instance._session = True
        logger.debug(locale('{driver_name}.transaction()',
            driver_name=self.instance.__class__.__name__
        ))

    def commit(self):
        """
        Отправляем изменения в базу данных

        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if not self.instance.connection:
            return None
        self.instance.connection.commit()
        self.instance._session = False
        logger.debug(locale('{driver_name}.commit()',
            driver_name=self.instance.__class__.__name__
        ))

    def flush(self):
        """
        Отправляем изменения в базу данных.

        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if not self.instance.connection:
            return None
        self.instance.connection.flush()
        logger.debug(locale('{driver_name}.flush()',
            driver_name=self.instance.__class__.__name__
        ))

    def rollback(self):
        """
        Отменяем изменения в базе данных

        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if not self.instance.connection:
            return None
        self.instance.connection.rollback()
        self.instance._session = False
        logger.debug(locale('{driver_name}.rollback()',
            driver_name=self.instance.__class__.__name__
        ))


class CommandDatabaseLinkDriver(DatabaseLinkDriver):
    """
    Link объект для управления схемами БД
    """

    def collections(self):
        """
        Получаем список таблиц в БД
        """
        return []

    def is_collection(self, check_collection):
        """
        Проверяем присутствует ли таблица в базе данных

        :param check_collection: Название таблицы.
        :return:
        """
        collections = self.instance.collections()
        is_exist = False
        for row in collections:
            if row == check_collection:
                is_exist = True
        return is_exist


class SchemaDatabaseLinkDriver(DatabaseLinkDriver):
    """
    Link объект для управления схемами БД
    """

    def add_collection(self):
        """
        Добавляем таблицу в базу данных

        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        try:
            if isinstance(self.instance._collection, Collection):
                result = self.instance.execute(self.instance._schema_table(self.instance._collection))
                if result and result.is_insert:
                    for inserted_primary_key in result.inserted_primary_key_rows:
                        return inserted_primary_key
                elif result and result.rowcount > 0:
                    for row in result:
                        logger.debug(locale('Колонка %s', row))
                else:
                    return
        except Exception as e:
            logger.exception(locale('Ошибка %s.add_collection()', self.instance.__class__.__name__))
            raise e

    def drop_collection(self, collection_name=None):
        """
        Удаляем таблицу из базы данных

        :param collection_name:
        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if collection_name is None:
            collection_name = self.instance._collection.collection_name
        try:
            return self.instance.execute(self.instance._drop_table(collection_name=collection_name))
        except Exception as e:
            logger.exception(locale('Ошибка %s.drop_collection()', self.instance.__class__.__name__))
            raise e

    def add_column(self, collection_name=None, after=None):
        """
        Добавляем поле в коллекцию в базу данных

        :param collection_name:
        :param after:
        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if collection_name is None:
            collection_name = self.instance._collection.collection_name
        try:
            if isinstance(self.instance._column, Column):
                return self.instance.execute(
                    self.instance._add_column(self.instance._column,
                                     after=after, collection_name=collection_name))
        except Exception as e:
            logger.exception(locale('Ошибка %s.add_column()', self.instance.__class__.__name__))
            raise e

    def drop_column(self, collection_name=None, column_name=None):
        """
        Удаляем поле из коллекции

        :param collection_name:
        :param column:
        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if collection_name is None:
            collection_name = self.instance._collection.collection_name
        try:
            return self.instance.execute(self.instance._drop_column(column=column_name, collection_name=collection_name))
        except Exception as e:
            logger.exception(locale('Ошибка %s.drop_column()', self.instance.__class__.__name__))
            raise e


class SchemaSqlDatabaseLinkDriver(DatabaseLinkDriver):
    """
    Link объект для управления схемами БД
    """

    def _schema_table(self, collection) -> str:
        """
        Определим схему таблицы основываясь на метаданных модели

        :param collection: Модель таблицы.
        :return: str
        """
        return None

    def _drop_table(self, collection_name=None) -> str:
        """
        Определим запрос для удаления таблицы опираясь на имя таблицы

        :param collection_name: Название таблицы
        :return: str
        """
        return None

    def _add_column(self, column, collection_name=None, after=None) -> str:
        """
        Определяет запрос добавления поля в таблицу

        :param column: Модель колонки.
        :param collection_name: Название таблицы.
        :param after: Название поля после которого вставить.
        :return: str
        """
        return None

    def _drop_column(self, column=None, collection_name=None) -> str:
        """
        Определяет запрос удаления поля из таблицы

        :param column: Название поля.
        :param collection_name: Название коллекции.
        :return: str
        """
        return None

    def _to_sql_type(self, column) -> str:
        """
        Определяет схему поля основываясь на метаданных модели поля

        :param column: Модель поля.
        :return: str
        """
        return None


class InsertDatabaseLinkDriver(DatabaseLinkDriver):
    """
    Link объект для функции добавления записей в бд
    """

    def insert(self):
        """
        Добавляем строку в базу данных

        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        try:
            print(isinstance(self.instance._model, Model))
            if isinstance(self.instance._model, Model):
                columns = self._sql_insert_columns(self.instance._model)
                values = self._sql_insert_values(self.instance._model)
                returning = self._sql_insert_returning(self.instance._model)
                query = self._sql_insert_query(self.instance._model, columns, values, returning)
                try:
                    result = self.instance.execute(query)
                    if hasattr(result, 'lastrowid'):
                        self._set_primary_key(self.instance._model, result.lastrowid)
                    else:
                        r = result.fetchone()
                        if len(r) == 1:
                            self._set_primary_key(self.instance._model, r[0])
                    return self.instance._model
                except Exception as e:
                    logger.exception(str(e))
                    return None
        except Exception as e:
            logger.exception(locale('Ошибка %s.insert()', self.instance.__class__.__name__))
            raise e

    def _set_primary_key(self, model, pk):
        """
        Заномим primary key в модель

        :param model: модель данных
        :param pk: значение primary key
        :return:
        """
        if hasattr(model, 'columns'):
            for column in model.columns:
                if isinstance(model.columns[column].field_type, Key) or model.columns[column].primary_key:
                    model.columns[column].value = pk
        return model

    def _sql_insert_query(self, model, columns, values, returning):
        """
        формируем запрос в базу данных для добавления строки

        :param model: модель
        :param columns: колонки данных
        :param values: значения данных
        :param returning: возвращаемое значение
        :return:
        """
        return "INSERT INTO {table} ({columns}) VALUES ({values}){returning}".format(
            table = model.collection,
            columns = ", ".join(columns),
            values = ", ".join(values),
            returning = " RETURNING {value}".format(value=", ".join(returning)) if returning else '',
        )

    def _sql_insert_returning(self, model):
        """
        Какое значение нужно вернуть

        :param model: модель
        :return:
        """
        columns = []
        if hasattr(model, 'columns'):
            for column in model.columns:
                if isinstance(model.columns[column].field_type, Key) or model.columns[column].primary_key:
                    columns.append('{value}'.format(value=model.columns[column].column_name))
        return columns

    def _sql_insert_columns(self, model):
        """
        Добавляемые колонки

        :param model: модель данных
        :return:
        """
        columns = []
        if hasattr(model, 'columns'):
            for column in model.columns:
                if isinstance(model.columns[column].field_type, Key) and model.columns[column].value is None:
                    pass
                else:
                    columns.append('{value}'.format(value=model.columns[column].column_name))
        return columns

    def _sql_insert_values(self, model):
        """
        Какие данные заносим

        :param model: модель данных
        :return:
        """
        values = []
        if hasattr(model, 'columns'):
            for column in model.columns:
                value = model.columns[column].value
                if isinstance(model.columns[column].field_type, Key) and value is None:
                    pass
                elif model.columns[column].field_type.data_type == 'enum' and value is not None:
                    print(column)
                    print(value)
                    print(model.columns[column].field_type)
                    print(model.columns[column].field_type.enums)
                    values.append("{value}".format(value=model.columns[column].field_type.enums.index(value)))
                elif isinstance(value, str) and model.columns[column].value.isnumeric():
                    values.append("{value}".format(value=value))
                elif isinstance(value, object):
                    values.append("'{value}'".format(value=str(value)))
                elif isinstance(value, str):
                    values.append("'{value}'".format(value=value))
                elif value is None:
                    values.append('null')
                elif isinstance(value, bool):
                    values.append('{value}'.format(value='true' if value else 'false'))
                else:
                    values.append('{value}'.format(value=value))
        return values


class DeleteDatabaseLinkDriver(DatabaseLinkDriver):
    """
    Link объект для функции удаления записей из базы данных
    """

    def delete(self):
        """
        Удаляем строку в базу данных

        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        try:
            if isinstance(self.instance._model, Model):
                where = self._sql_delete_where(self.instance._model)
                query = self._sql_delete_query(self.instance._model, where)
                try:
                    result = self.instance.execute(query)
                    return self.instance._model
                except Exception as e:
                    logger.exception(str(e))
                    return None
        except Exception as e:
            logger.exception(locale('Ошибка %s.insert()', self.instance.__class__.__name__))
            raise e

    def _sql_delete_query(self, model, where):
        """
        формируем запрос в базу данных для удаления строки

        :param model: модель
        :param where: запрос поиска строк
        :return:
        """
        return "DELETE FROM {table} WHERE {where}".format(
            table = model.collection,
            where = " and ".join(where),
        )

    def _sql_delete_where(self, model):
        """
        Формирует запрос для поиска строк для удаления

        :param model: модель
        :return:
        """
        columns = []
        if hasattr(model, 'columns'):
            for column in model.columns:
                if (isinstance(model.columns[column].field_type, Key) or model.columns[column].primary_key):
                    value = model.columns[column].value
                    if isinstance(value, object):
                        value = "'{value}'".format(value=str(value))
                    elif isinstance(value, str):
                        value = "'{value}'".format(value=str(value))
                    elif value is None:
                        value = "null"
                    elif isinstance(value, bool):
                        value = "{value}".format(value='true' if value else 'false')
                    columns.append('{key}={value}'.format(
                        key=model.columns[column].column_name,
                        value=value
                    ))
        return columns


class UpdateDatabaseLinkDriver(DatabaseLinkDriver):
    """
    Link объект для функции обновления записей из базы данных
    """

    def update(self):
        """
        Обновляем строку в базе данных

        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        try:
            if isinstance(self.instance._model, Model):
                where = self._sql_update_where(self.instance._model)
                columns = self._sql_update_columns(self.instance._model)
                query = self._sql_update_query(self.instance._model, columns, where)
                try:
                    result = self.instance.execute(query)
                    return self.instance._model
                except Exception as e:
                    logger.exception(str(e))
                    return None
        except Exception as e:
            logger.exception(locale('Ошибка %s.insert()', self.instance.__class__.__name__))
            raise e

    def _sql_update_query(self, model, columns, where):
        """
        формируем запрос в базу данных для удаления строки

        :param model: модель
        :param columns: колонки для изменения
        :param where: запрос поиска строк
        :return:
        """
        return "UPDATE {table} SET {columns} WHERE {where}".format(
            table = model.collection,
            where = " and ".join(where),
            columns = ", ".join(columns),
        )

    def _sql_update_columns(self, model):
        """
        Определяем колонки для изменения

        :param model: модель данных
        :return:
        """
        columns = []
        if hasattr(model, 'columns'):
            for column in model.columns:
                value = model.columns[column].value
                if isinstance(model.columns[column].field_type, Key) and value is None:
                    pass
                elif isinstance(value, str) and model.columns[column].value.isnumeric():
                    columns.append("{column_name}={value}".format(
                        value=value,
                        column_name=model.columns[column].column_name
                    ))
                elif isinstance(value, object):
                    columns.append("{column_name}='{value}'".format(
                        value=str(value),
                        column_name=model.columns[column].column_name
                    ))
                elif isinstance(value, str):
                    columns.append("{column_name}='{value}'".format(
                        value=value,
                        column_name=model.columns[column].column_name
                    ))
                elif value is None:
                    columns.append("{column_name}={value}".format(
                        value='null',
                        column_name=model.columns[column].column_name
                    ))
                elif isinstance(value, bool):
                    columns.append('{column_name}={value}'.format(
                        value='true' if value else 'false',
                        column_name=model.columns[column].column_name
                    ))
                else:
                    columns.append('{column_name}={value}'.format(
                        value=value,
                        column_name=model.columns[column].column_name
                    ))
        return columns

    def _sql_update_where(self, model):
        """
        Формирует запрос для поиска строк для удаления

        :param model: модель
        :return:
        """
        columns = []
        if hasattr(model, 'columns'):
            for column in model.columns:
                if (isinstance(model.columns[column].field_type, Key) or model.columns[column].primary_key):
                    value = model.columns[column].value
                    if isinstance(value, object):
                        value = "'{value}'".format(value=str(value))
                    elif isinstance(value, str):
                        value = "'{value}'".format(value=str(value))
                    elif value is None:
                        value = "null"
                    elif isinstance(value, bool):
                        value = "{value}".format(value='true' if value else 'false')
                    columns.append('{key}={value}'.format(
                        key=model.columns[column].column_name,
                        value=value
                    ))
        return columns


class FindDatabaseLinkDriver(DatabaseLinkDriver):
    """
    Link объект для функции поиска записей из базы данных
    """

    def find(self, query):
        """
        Обновляем строку в базе данных

        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        try:
            model = self.instance._model()
            models = []
            if isinstance(model, Model):
                where = self._sql_find_where(model, query)
                query = self._sql_find_query(model, where)
                try:
                    result = self.instance.execute(query)
                    for r in result.mappings().all():
                        model = self.instance._model()
                        models.append(self._fetch_model(model, r))
                    return models
                except Exception as e:
                    logger.exception(str(e))
                    return None
        except Exception as e:
            logger.exception(locale('Ошибка %s.insert()', self.instance.__class__.__name__))
            raise e

    def _fetch_model(self, model, result):
        """
        Заполняем модель

        :param model: модель
        :param result: результат запроса к базе
        :return:
        """
        if hasattr(model, 'columns'):
            for column in model.columns:
                if column in result:
                    model.columns[column].value = result[column]
        return model

    def _sql_find_query(self, model, where):
        """
        формируем запрос в базу данных для удаления строки

        :param model: модель
        :param columns: колонки для изменения
        :param where: запрос поиска строк
        :return:
        """
        return "SELECT * FROM {table} WHERE {where}".format(
            table = model.collection,
            where = " and ".join(where),
        )

    def _sql_find_where(self, model, query):
        columns = []
        for q in query:
            if isinstance(query[q], str) and query[q].isnumeric():
                value = query[q]
            elif isinstance(query[q], str):
                value = "'{value}'".format(value=query[q])
            elif isinstance(query[q], object):
                value = "'{value}'".format(value=str(query[q]))
            elif isinstance(query[q], bool):
                value = "{value}".format(value='true' if query[q] else 'false')
            elif query[q] is None:
                value = "null"
            else:
                value = "{value}".format(value=query[q])
            columns.append("{column}={value}".format(column=q, value=value))
        return columns

