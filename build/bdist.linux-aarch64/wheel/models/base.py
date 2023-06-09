import inspect


class BaseCollection(object):
    pass


# class Model(BaseType):
#
#     def __init__(self, node_name, *columns):
#         self.node_name = node_name
#         self.columns = columns


class Collection(BaseCollection):

    def __init__(self, collection_name, *columns):
        self.collection_name = collection_name
        self.columns = columns


class BaseColumn(object):
    pass


class Column(BaseColumn):

    def __set_name__(self, owner, name):
        self.column_name = name
        if not hasattr(owner, 'columns'):
            setattr(owner, 'columns', dict())
        owner.columns[name] = self

    def __init__(self, *args, index=False, unique=False, primary_key=False, nullable=False, default=None,
                 required=False, title=None, description=None, example=None):
        if len(args) > 1:
            self.column_name = args[0]
            self.field_type = args[1] if not callable(args[1]) else args[1]()
        elif len(args) == 1:
            self.field_type = args[0] if not callable(args[0]) else args[0]()

        self.index = index
        self.unique = unique
        self.default = default
        self.required = required
        self.title = title
        self.description = description
        self.nullable = nullable
        self.value = self.default
        self.primary_key = primary_key
        self.example = example


    def __set__(self, instance, value):
        self.value = value

    def __get__(self, instance, owner):
        return self.value


class BaseField(object):
    pass


class Boolean(BaseField):

    data_type = 'boolean'

    def __init__(self):
        pass


class Numeric(BaseField):

    data_type = 'numeric'

    def __init__(self, precision=None, scale=None, decimal_return_scale=None, asdecimal=True):
        self.precision = precision,
        self.scale = scale,
        self.decimal_return_scale = decimal_return_scale,
        self.asdecimal = asdecimal


class Float(BaseField):

    data_type = 'float'

    def __init__(self, precision=None, asdecimal=False, decimal_return_scale=None):
        self.precision = precision
        self.asdecimal = asdecimal
        self.decimal_return_scale = decimal_return_scale


class Binary(BaseField):

    data_type = 'binary'

    def __init__(self, length=None):
        self.length = length


class Enum(BaseField):

    data_type = 'enum'

    def __set_name__(self, owner, name):
        self.enum_name = name

    def __init__(self, enums=None):
        # if not self.enum_name:
        #     self.enum_name = type(self).__name__
        self.enums = enums


# class Enum(BaseField):
#
#     data_type = 'enum'
#
#     def __init__(self, enums=None):
#         self.enums = enums


class Key(BaseField):

    data_type = 'key'

    def __init__(self):
        pass


class BigInteger(BaseField):

    data_type = 'big_integer'

    def __init__(self, length=None):
        self.length = length


class SmallInteger(BaseField):

    data_type = 'small_integer'

    def __init__(self, length=None):
        self.length = length


class Integer(BaseField):

    data_type = 'integer'

    def __init__(self, length=None):
        self.length = length


class String(BaseField):

    data_type = 'string'

    def __init__(self, length=255):
        self.length = length


class Date(BaseField):

    data_type = 'date'

    def __init__(self):
        pass


class DateTime(BaseField):

    data_type = 'date_time'

    def __init__(self, timezone=None):
        self.timezone = timezone


class Timestamp(BaseField):

    data_type = 'timestamp'

    def __init__(self, timezone=None):
        self.timezone = timezone


class Time(BaseField):

    data_type = 'time'

    def __init__(self, timezone=None):
        self.timezone = timezone


class Text(BaseField):

    data_type = 'text'

    def __init__(self, length=65535):
        self.length = length

