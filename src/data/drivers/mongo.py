from datetime import datetime

import pymongo
from bson import ObjectId
from pymongo.database import Database

from ...models import Model, Key
from ...models import Collection, Column
from ..driver import CRUDDatabaseLinkDriver, DatabaseLinkDriver, DataDriver, DataDatabaseLinkDriver
from ...storage import StorageMapper
from bson.timestamp import Timestamp

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
        url = "{driver}://{user}:{password}@{host}:{port}/".format(
            driver=config.driver,
            host=config.host,
            port=config.port,
            user=config.user,
            password=config.password,
        )
        logger.debug(locale("Подключаемся {driver_name}.connect({url})",
            driver_name=self.instance.__class__.__name__,
            url=url
        ))
        self.instance.url = url
        client = pymongo.MongoClient(url)
        db = getattr(client, str(config.database))
        self.instance.engine = client
        self.instance.connection = db
        return self.instance

    def get_url(self):
        return self.instance.url


class ExecuteDatabaseLinkDriver(DatabaseLinkDriver):
    """
    Link объект для подключения к БД
    """

    def execute(self, query, params=None):
        """
        Выполняет запрос в базу данных Mongo

        :param query: dict
        :param params: dict
        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if not isinstance(self.instance.connection, Database):
            return None
        logger.debug(locale('{driver_name}.execute("{query}", {params})',
            query=query,
            params=params,
            driver_name=self.instance.__class__.__name__
        ))
        return self.instance.connection.execute(query, params)


class TransactionDatabaseLinkDriver(DatabaseLinkDriver):
    """
    Link объект для подключения к БД
    """

    def __init__(self, instance):
        """
        Устанавливаем значения по умолчанию

        :param instance:
        """
        super().__init__(instance)
        if not hasattr(self.instance, '_session'):
            self.instance._session = False

    def transaction(self):
        """
        Включает режим транзакций

        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if not isinstance(self.instance.connection, Database):
            raise Exception(locale('`connection` должен быть определен объектом Database'))
        self.instance._session = self.instance.engine.start_session()
        self.instance._session.start_transaction()
        logger.debug(locale('{driver_name}.transaction()',
            driver_name = self.instance.__class__.__name__
        ))

    def commit(self):
        """
        Заносит все изменения в базу данных в режиме транзакций. После занесения режим транзакций выключается

        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if not self.instance._session:
            return None
        self.instance._session.commit_transaction()
        self.instance._session.end_session()
        self.instance._session = None
        logger.debug(locale('{driver_name}.commit()',
            driver_name=self.instance.__class__.__name__
        ))

    def flush(self):
        """


        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if not self.instance._session:
            return None
        self.instance._session.commit_transaction()
        logger.debug(locale('{driver_name}.flush()',
            driver_name=self.instance.__class__.__name__
        ))

    def rollback(self):
        """
        Откатывает изменения к базе данных в режиме транзакций. После отката режим транзакций отключается.

        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if not self.instance._session:
            return None
        self.instance._session.abort_transaction()
        self.instance._session.end_session()
        self.instance._session = None
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
        if not isinstance(self.instance.connection, Database):
            raise Exception('`connection` должен быть определен объектом Database')
        collections = []
        for row in self.instance.connection.list_collection_names():
            collections.append(row)
        return collections

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
        Добавляем колекцию в базу данных
        renameCollection

        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if not isinstance(self.instance.connection, Database):
            raise Exception(locale('`connection` должен быть определен объектом Database'))
        try:
            if isinstance(self.instance._collection, Collection):
                collection = self.instance._schema_collection(self.instance._collection)
                logger.debug(locale('{driver_name}.add_collection/create_collection({collection_name})',
                    collection_name=collection[0],
                    driver_name=self.instance.__class__.__name__
                ))
                result = self.instance.connection.create_collection(collection[0], validator=collection[1]['validator'])
                for column in self.instance._collection.columns:
                    if column.index or column.unique:
                        self.instance.create_index(collection[0], column.column_name, unique=column.unique)
                return result
            raise Exception(locale('`collection` должен быть определен объектом Collection'))
        except Exception as e:
            logger.exception(locale('Ошибка во время выполнения {driver_name}.{action}',
                action='add_collection',
                driver_name=self.instance.__class__.__name__
            ))
            raise e

    def drop_collection(self, collection_name=None):
        """
        Удаляем коллекцию из базы данных

        :param collection_name:
        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if not isinstance(self.instance.connection, Database):
            raise Exception(locale('`connection` должен быть определен объектом Database'))
        if collection_name is None:
            collection_name = self.instance._collection.collection_name
        try:
            if self.instance.is_collection(collection_name):
                logger.debug(locale('{driver_name}.drop_collection/drop_collection({collection_name})',
                    collection_name=collection_name,
                    driver_name=self.instance.__class__.__name__
                ))
                return self.instance.connection.drop_collection(collection_name)
            else:
                raise Exception(locale('Коллекции {collection_name} не существует', collection_name=collection_name))
        except Exception as e:
            logger.exception(locale('Ошибка во время выполнения {driver_name}.{action}',
                action='drop_collection',
                driver_name=self.instance.__class__.__name__
            ))
            raise e

    def create_index(self, collection_name=None, column_name=None, unique=False):
        """
        Создаем индекс в базе данных

        :param collection_name:
        :param column_name:
        :param unique:
        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if self.instance.is_collection(collection_name) and not self.instance.is_index(
                collection_name=collection_name, index_name=column_name):
            logger.debug(locale('{driver_name}.create_index/create_index({collection_name}, {column_name})',
                collection_name=collection_name,
                column_name=column_name,
                driver_name=self.instance.__class__.__name__
            ))
            return self.instance.connection[collection_name].create_index(column_name, name=column_name, unique=unique)
        return None

    def drop_index(self, collection_name=None, column_name=None):
        """
        Удаляем индекс из базы данных

        :param collection_name:
        :param column_name:
        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if self.instance.is_collection(collection_name) and self.instance.is_index(
                collection_name=collection_name, index_name=column_name):
            logger.debug(locale('{driver_name}.drop_index/drop_index({collection_name}, {column_name})',
                collection_name=collection_name,
                column_name=column_name,
                driver_name=self.instance.__class__.__name__
            ))
            return self.instance.connection[collection_name].drop_index(column_name)
        return None

    def index_list(self, collection_name=None):
        """
        Получаем список индексов в базе данных

        :param collection_name:
        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if self.instance.is_collection(collection_name):
            logger.debug(locale('{driver_name}.index_information/index_list({collection_name})',
                collection_name=collection_name,
                driver_name=self.instance.__class__.__name__
            ))
            inx = self.instance.connection[collection_name].index_information()
            return inx.keys()
        return None

    def is_index(self, collection_name=None, index_name=None):
        """
        Проверяем существует ли индекс в базе данных

        :param collection_name:
        :param index_name:
        :return:
        """
        indexes = self.instance.index_list(collection_name=collection_name)
        if index_name in indexes:
            return True
        return False

    def add_column(self, collection_name=None, after=None):
        """
        Создаем колонку в базе данных в определенной коллекции

        :param collection_name:
        :param after:
        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if not isinstance(self.instance.connection, Database):
            raise Exception(locale('`connection` должен быть определен объектом Database'))
        if collection_name is None:
            collection_name = self.instance._collection.collection_name
        try:
            if isinstance(self.instance._column, Column):
                column = self.instance._schema_column(self.instance._column)
                validator_schema = self.instance._get_schema_validator(collection_name)
                if validator_schema:
                    validator_schema['properties'][self.instance._column.column_name] = column[1][self.instance._column.column_name]
                if column[0] and self.instance._column.column_name not in validator_schema['required']:
                    validator_schema['required'].append(self.instance._column.column_name)
                if column.index or column.unique:
                    self.instance.create_index(collection_name, self.instance._column.column_name, unique=self.instance._column.unique)
                if self.instance.is_collection(collection_name):
                    logger.debug(locale('{driver_name}.command/add_column({collection_name}, {type})',
                        collection_name=collection_name,
                        type='$jsonSchema',
                        driver_name=self.instance.__class__.__name__
                    ))
                    return self.instance.connection.command({
                        "collMod": collection_name,
                        "validator": {
                            "$jsonSchema": {
                                "bsonType": validator_schema['bsonType'],
                                "required": validator_schema['required'],
                                "properties": validator_schema['properties']
                            }
                        }
                    })
                else:
                    raise Exception(locale('Коллекции {collection_name} не существует',
                                           collection_name=collection_name))
            else:
                raise Exception(locale('`column` должен быть определен объектом Column'))
        except Exception as e:
            logger.exception(locale('Ошибка во время выполнения {driver_name}.{action}',
                action='add_column',
                driver_name=self.instance.__class__.__name__
            ))
            raise e

    def drop_column(self, collection_name=None, column_name=None):
        """
        Удаляем колонку из базы данных в определенной коллекции

        :param collection_name:
        :param column_name:
        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        if not isinstance(self.instance.connection, Database):
            raise Exception(locale('`connection` должен быть определен объектом Database'))
        if collection_name is None:
            collection_name = self.instance._collection.collection_name
        try:
            if column_name is not None:
                validator_schema = self.instance._get_schema_validator(collection_name)
                if validator_schema and validator_schema['properties'].get(column_name):
                    del validator_schema['properties'][column_name]
                if column_name in validator_schema['required']:
                    del validator_schema['required'][validator_schema['required'].index(column_name)]
                if self.instance.is_collection(collection_name):
                    self.instance.drop_index(collection_name=collection_name, column_name=column_name)
                    logger.debug(locale('{driver_name}.command/drop_column({collection_name}, {type})',
                        collection_name=collection_name,
                        type='$jsonSchema',
                        driver_name=self.instance.__class__.__name__
                    ))
                    return self.instance.connection.command({
                        "collMod": collection_name,
                        "validator": {
                            "$jsonSchema": {
                                "bsonType": validator_schema['bsonType'],
                                "required": validator_schema['required'],
                                "properties": validator_schema['properties']
                            }
                        }
                    })
                else:
                    raise Exception(locale('Коллекции {collection_name} не существует',
                                           collection_name=collection_name))
            else:
                raise Exception(locale('`column_name` должен быть указан'))
        except Exception as e:
            logger.exception(locale('Ошибка во время выполнения {driver_name}.{action}',
                action='drop_column',
                driver_name=self.instance.__class__.__name__
            ))
            raise e


class SchemaMongoDatabaseLinkDriver(DatabaseLinkDriver):
    """
    Link объект для управления схемами БД
    """

    def _get_schema_collections(self):
        b = self.instance.connection.command({'listCollections': 1})
        if b['ok']:
            firstBatch = b['cursor']['firstBatch']
            return firstBatch
        else:
            return []

    def _get_schema_collection(self, collection):
        collection_schema = None
        collections = self.instance._get_schema_collections()
        for _collection in collections:
            if collection == _collection['name']:
                collection_schema = _collection['options']
        return collection_schema

    def _get_schema_validator(self, collection):
        validator_schema = None
        collection = self.instance._get_schema_collection(collection)
        if collection:
            validator_schema = collection['validator']['$jsonSchema']
        return validator_schema

    def _schema_collection(self, collection) -> tuple:
        """
        Определим схему таблицы основываясь на метаданных модели

        :param collection: Модель таблицы.
        :return: tuple
        """
        columns = {}
        required = []
        for column in collection.columns:
            columns.update(self._to_json_schema(column))
            if column.required:
                required.append(column.column_name)

        schema = {
            "validator": {
                "$jsonSchema": {
                    "bsonType": "object",
                }
            }
        }

        if required:
            schema['validator']['$jsonSchema']['required'] = required

        if columns:
            schema['validator']['$jsonSchema']['properties'] = columns

        return (collection.collection_name, schema)

    def _schema_column(self, column) -> tuple:
        """
        Определим схему таблицы основываясь на метаданных модели

        :param collection: Модель таблицы.
        :return: tuple
        """
        _column = {}
        _column = self.instance._to_json_schema(column)
        return column.required, _column

    def _to_json_schema(self, column) -> dict:
        """
        Возвращает схему поля по модели поля

        :param column: Модель поля
        :return: dict
        """
        t = dict()
        if column.field_type.data_type == 'key':
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "objectId",
                "description": column.description if column.description else ''
            }
            pass
        elif column.field_type.data_type == 'integer':
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "int",
                "description": column.description if column.description else ''
            }
        elif column.field_type.data_type == 'big_integer':
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "long",
                "description": column.description if column.description else ''
            }
        elif column.field_type.data_type == 'string':
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "string",
                "description": column.description if column.description else ''
            }
        elif column.field_type.data_type == 'text':
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "string",
                "description": column.description if column.description else ''
            }
        elif column.field_type.data_type == 'date':
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "date",
                "description": column.description if column.description else ''
            }
        elif column.field_type.data_type == 'date_time':
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "timestamp",
                "description": column.description if column.description else ''
            }
        elif column.field_type.data_type == 'timestamp':
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "timestamp",
                "description": column.description if column.description else ''
            }
        elif column.field_type.data_type == 'time':
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "timestamp",
                "description": column.description if column.description else ''
            }
        elif column.field_type.data_type == 'year':
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "int",
                "description": column.description if column.description else ''
            }
        elif column.field_type.data_type == 'binary':
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "binData",
                "description": column.description if column.description else ''
            }
        elif column.field_type.data_type == 'enum':
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "string",
                "description": column.description if column.description else '',
                "enum": column.field_type.enums,
            }
        elif column.field_type.data_type == 'small_integer':
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "int",
                "description": column.description if column.description else ''
            }
        elif column.field_type.data_type == 'boolean':
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "bool",
                "description": column.description if column.description else ''
            }
        elif column.field_type.data_type == 'float':
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "double",
                "description": column.description if column.description else ''
            }
        elif column.field_type.data_type == 'numeric':
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "decimal",
                "description": column.description if column.description else ''
            }
        elif column.field_type.data_type == 'object':
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "object",
                "description": column.description if column.description else '',
                "properties": {

                }
            }
        else:
            t[column.column_name] = {
                "title": column.column_name,
                "bsonType": "mixed",
                "description": column.description if column.description else ''
            }
        return t



class DocumentSchemaDatabaseLinkDriver(DatabaseLinkDriver):
    """
    Link объект для функции добавления записей в бд
    """

    def _document_schema(self, model, ignore_key=False):
        """
        Добавляем строку в базу данных

        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        try:
            if isinstance(model, Model):
                data = {}
                if hasattr(model, 'columns'):
                    for column in model.columns:
                        value = model.columns[column].value
                        data_type = model.columns[column].field_type.data_type
                        if isinstance(model.columns[column].field_type, Key) or model.columns[column].primary_key:
                            if not ignore_key:
                                data.update({'_id': value})
                        elif data_type == 'timestamp' and value is not None:
                            data.update({column: Timestamp(int(value.timestamp()), 1)})
                        elif data_type == 'enum' and value is not None:
                            data.update({column: value})
                        elif isinstance(value, str) and value.isnumeric():
                            data.update({column: value})
                        elif isinstance(value, object):
                            data.update({column: str(value)})
                        elif isinstance(value, str):
                            data.update({column: value})
                        elif value is None:
                            data.update({column: None})
                        elif isinstance(value, bool):
                            data.update({column: True if value else False})
                        else:
                            data.update({column: value})
                return data
        except Exception as e:
            logger.exception(locale('Ошибка %s.insert()', self.instance.__class__.__name__))
            raise e


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
            if isinstance(self.instance._model, Model):
                data = self.instance._document_schema(self.instance._model, ignore_key=True)
                try:
                    logger.debug(locale('{driver_name}.insert_one({data})',
                        data=data,
                        driver_name=self.instance.__class__.__name__
                    ))
                    collection = self.instance._model.collection
                    result = self.instance.connection[collection].insert_one( data )
                    self._set_primary_key(self.instance._model, str(result.inserted_id))
                    return str(result.inserted_id)
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
                filter = {}
                for column in self.instance._model.columns:
                    if isinstance(self.instance._model.columns[column].field_type, Key):
                        filter.update({'_id': ObjectId(self.instance._model.columns[column].value)})
                try:
                    logger.debug(locale('{driver_name}.delete_one({filter})',
                        filter=filter,
                        driver_name=self.instance.__class__.__name__
                    ))
                    collection = self.instance._model.collection
                    result = self.instance.connection[collection].delete_one( filter )
                    return result.deleted_count
                except Exception as e:
                    logger.exception(str(e))
                    return None
        except Exception as e:
            logger.exception(locale('Ошибка %s.delete()', self.instance.__class__.__name__))
            raise e

class UpdateDatabaseLinkDriver(DatabaseLinkDriver):
    """
    Link объект для функции обновления записей из базы данных
    """

    def update(self):
        """
        Обновляем строку в базу данных

        :return:
        """
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        try:
            if isinstance(self.instance._model, Model):
                data = self.instance._document_schema(self.instance._model, ignore_key=True)
                filter = {}
                data = {"$set": data}
                for column in self.instance._model.columns:
                    if isinstance(self.instance._model.columns[column].field_type, Key):
                        filter.update({'_id': ObjectId(self.instance._model.columns[column].value)})
                try:
                    logger.debug(locale('{driver_name}.update_one({filter}, {data}, upsert=True)',
                        data=data,
                        filter=filter,
                        driver_name=self.instance.__class__.__name__
                    ))
                    collection = self.instance._model.collection
                    result = self.instance.connection[collection].update_one( filter, data, upsert=True )
                    return result.modified_count
                except Exception as e:
                    logger.exception(str(e))
                    return None
        except Exception as e:
            logger.exception(locale('Ошибка %s.update()', self.instance.__class__.__name__))
            raise e


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
        models = []
        try:
            model = self.instance._model()
            if isinstance(model, Model):
                filter = self._find_filter(model, query)
                try:
                    logger.debug(locale('{driver_name}.find({filter})',
                        filter=filter,
                        driver_name=self.instance.__class__.__name__
                    ))
                    collection = model.collection
                    result = self.instance.connection[collection].find( filter )
                    for r in result:
                        models.append(self._fetch_model(model, r))
                    return models
                except Exception as e:
                    logger.exception(str(e))
                    return models
        except Exception as e:
            logger.exception(locale('Ошибка %s.find()', self.instance.__class__.__name__))
            raise e


    def _find_filter(self, model, query):
        locale = storageMapper.get('locale')
        logger = storageMapper.get('logger')
        columns = {}
        for q in query:
            if not hasattr(model, q):
                raise Exception(locale('Поле %s не найдено', q))
            else:
                column = model.columns[q]
            if isinstance(column.field_type, Key) or column.primary_key:
                value = ObjectId(query[q])
                q = '_id'
            elif isinstance(query[q], str) and query[q].isnumeric():
                value = query[q]
            elif isinstance(query[q], str):
                value = str(query[q])
            elif isinstance(query[q], object):
                value = str(query[q])
            else:
                value = query[q]
            columns.update({q: value})
        return columns

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


class MongoDB(DataDriver):
    """
    Драйвер для базы данных Postgres. Механизм реализуется через sqlalchemy.

    """

    def __init__(self, name=None):
        super().__init__(name=name)
        self.name = name
        self._mappers = [
            TransactionDatabaseLinkDriver(self),
            LinkDatabaseLinkDriver(self),
            ExecuteDatabaseLinkDriver(self),
            CommandDatabaseLinkDriver(self),
            SchemaDatabaseLinkDriver(self),
            CRUDDatabaseLinkDriver(self),
            SchemaMongoDatabaseLinkDriver(self),
            DataDatabaseLinkDriver(self),
            DocumentSchemaDatabaseLinkDriver(self),
            InsertDatabaseLinkDriver(self),
            DeleteDatabaseLinkDriver(self),
            UpdateDatabaseLinkDriver(self),
            FindDatabaseLinkDriver(self),
        ]


