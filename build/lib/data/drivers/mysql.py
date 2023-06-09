from ..driver import CRUDDatabaseLinkDriver, DatabaseLinkDriver, DataDriver, DataDatabaseLinkDriver
from .sql_link_driver import LinkDatabaseLinkDriver, ExecuteDatabaseLinkDriver, TransactionDatabaseLinkDriver, \
    CommandDatabaseLinkDriver, SchemaDatabaseLinkDriver
from ...storage import StorageMapper
from .sql_link_driver import InsertDatabaseLinkDriver, UpdateDatabaseLinkDriver, \
    DeleteDatabaseLinkDriver, FindDatabaseLinkDriver
storageMapper = StorageMapper()


class CommandMysqlDatabaseLinkDriver(CommandDatabaseLinkDriver):
    """
    Link объект для управления схемами БД
    """

    def collections(self):
        """
        Получаем список таблиц в БД
        """
        result = self.instance.execute("SHOW TABLES;")
        collections = []
        for row in result:
            collections.append(row[0])
        return collections


class SchemaMysqlDatabaseLinkDriver(DatabaseLinkDriver):
    """
    Link объект для управления схемами БД
    """

    def _schema_table(self, collection) -> str:
        """
        Определим схему таблицы основываясь на метаданных модели

        :param collection: Модель таблицы.
        :return: str
        """
        columns = []
        for column in collection.columns:
            columns.append(self._to_sql_type(column))
        return "CREATE TABLE {collection_name} ({columns});".format(
            collection_name=collection.collection_name,
            columns=', '.join(columns)
        )

    def _drop_table(self, collection_name=None) -> str:
        """
        Определим запрос для удаления таблицы опираясь на имя таблицы

        :param collection_name: Название таблицы
        :return: str
        """
        return "DROP TABLE {collection_name};".format(
            collection_name=collection_name
        )

    def _add_column(self, column, collection_name=None, after=None) -> str:
        """
        Определяет запрос добавления поля в таблицу

        :param column: Модель колонки.
        :param collection_name: Название таблицы.
        :param after: Название поля после которого вставить.
        :return: str
        """
        return "ALTER TABLE {collection_name} ADD {column};".format(
            collection_name=collection_name,
            column=self._to_sql_type(column)
        )

    def _drop_column(self, column=None, collection_name=None) -> str:
        """
        Определяет запрос удаления поля из таблицы

        :param column: Название поля.
        :param collection_name: Название коллекции.
        :return: str
        """
        return "ALTER TABLE {collection_name} DROP {column};".format(
            collection_name=collection_name,
            column=column
        )

    def _to_sql_type(self, column) -> str:
        """
        Определяет схему поля основываясь на метаданных модели поля

        :param column: Модель поля.
        :return: str
        """
        col = "{column_name} {field}{field_param} {nullable} {default} {index}"
        field_param = ''
        index = ''
        if hasattr(column.field_type, 'length'):
            field_param = '({value})'.format(value=column.field_type.length) if column.field_type.length is not None else ''

        if column.field_type.data_type == 'key':
            field='BIGINT'
            field_param = '(16)'
            index='primary key AUTO_INCREMENT'
        elif column.field_type.data_type == 'integer':
            field='INTEGER'
            field_param = ''
        elif column.field_type.data_type == 'big_integer':
            field='BIGINT'
        elif column.field_type.data_type == 'string':
            field='VARCHAR'
        elif column.field_type.data_type == 'text':
            field='TEXT'
            field_param = '({value})'.format(value=column.field_type.length) if column.field_type.length is not None else 65535
        elif column.field_type.data_type == 'date':
            field='DATE'
            field_param = ''
        elif column.field_type.data_type == 'date_time':
            field='TIMESTAMP'
            field_param='({value})'.format(value=column.field_type.timezone) if column.field_type.timezone is not None else ''
        elif column.field_type.data_type == 'timestamp':
            field='TIMESTAMP'
            field_param='({value})'.format(value=column.field_type.timezone) if column.field_type.timezone is not None else ''
        elif column.field_type.data_type == 'time':
            field='TIME'
            field_param='({value})'.format(value=column.field_type.timezone) if column.field_type.timezone is not None else ''
        elif column.field_type.data_type == 'year':
            field='YEAR'
            field_param = ''
        elif column.field_type.data_type == 'binary':
            field='BLOB'
        elif column.field_type.data_type == 'enum':
            field='ENUM'
            field_param = "('{value}')".format(value="', '".join(column.field_type.enums))
        elif column.field_type.data_type == 'small_integer':
            field='INTEGER'
        elif column.field_type.data_type == 'boolean':
            field='BOOLEAN'
            field_param = ''
        elif column.field_type.data_type == 'float':
            field='FLOAT'
            field_param='({value})'.format(value=column.field_type.precision) if column.field_type.precision else ''
        elif column.field_type.data_type == 'numeric':
            field='DECIMAL'
            field_param='({length}, {precision})'.format(
                length=column.field_type.length or 11,
                precision=column.field_type.precision or 5
            ) if column.field_type.length or column.field_type.precision else ''
        else:
            field='VARCHAR'

        t = col.format(
            field=field,
            column_name=column.column_name,
            default='DEFAULT "{value}"'.format(value=column.default) if column.default is not None else '',
            nullable='NOT NULL' if column.nullable else '',
            field_param=field_param,
            index=index,
        )
        return t


class InsertMysqlDatabaseLinkDriver(InsertDatabaseLinkDriver):
    """
    Link объект для функции добавления записей в бд
    """

    def _sql_insert_query(self, model, columns, values, returning):
        """
        формируем запрос в базу данных для добавления строки

        :param model: модель
        :param columns: колонки данных
        :param values: значения данных
        :param returning: возвращаемое значение
        :return:
        """
        return "INSERT INTO {table} ({columns}) VALUES ({values})".format(
            table = model.collection,
            columns = ", ".join(columns),
            values = ", ".join(values),
        )


class Mysql(DataDriver):
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
            CommandMysqlDatabaseLinkDriver(self),
            SchemaDatabaseLinkDriver(self),
            CRUDDatabaseLinkDriver(self),
            SchemaMysqlDatabaseLinkDriver(self),
            DataDatabaseLinkDriver(self),
            InsertMysqlDatabaseLinkDriver(self),
            DeleteDatabaseLinkDriver(self),
            UpdateDatabaseLinkDriver(self),
            FindDatabaseLinkDriver(self),
        ]


