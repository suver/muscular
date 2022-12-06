from .schema import Schema


class BaseField(Schema):

    schema_type = None
    data_type = None
    data_format = None

    def __init__(self, *args, **kwargs):
        if self.schema_type is None:
            self.schema_type = self.data_type
        super().__init__(*args, **kwargs)

    def dump(self) -> dict:
        results = super().dump()
        results.update({
            "data_type": self.data_type,
            "type": self.schema_type,
            "format": self.data_format,
        })
        return results


class Boolean(BaseField):

    data_type = 'boolean'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class List(BaseField):

    data_type = 'array'

    def __init__(self, *args, **kwargs):
        self._items = args[0] or None
        super().__init__(*args, **kwargs)

    def dump(self) -> dict:
        results = super().dump()
        results.update({
            "items": [self._items.dump()],
        })
        return results


class Numeric(BaseField):

    data_type = 'number'

    def __init__(self, *args, precision=None, scale=None, decimal_return_scale=None, asdecimal=True, **kwargs):
        kwargs['precision'] = precision
        kwargs['scale'] = scale
        kwargs['decimal_return_scale'] = decimal_return_scale
        kwargs['asdecimal'] = asdecimal
        super().__init__(*args, **kwargs)
        self.precision = precision
        self.scale = scale
        self.decimal_return_scale = decimal_return_scale
        self.asdecimal = asdecimal

    def dump(self) -> dict:
        results = super().dump()
        results.update({
            "precision": self.precision,
            "scale": self.scale,
            "decimal_return_scale": self.decimal_return_scale,
            "asdecimal": self.asdecimal,
        })
        return results


class Float(BaseField):

    data_type = 'float'

    def __init__(self, *args, precision=None, decimal_return_scale=None, asdecimal=True, **kwargs):
        kwargs['precision'] = precision
        kwargs['decimal_return_scale'] = decimal_return_scale
        kwargs['asdecimal'] = asdecimal
        super().__init__(*args, **kwargs)
        self.precision = precision
        self.asdecimal = asdecimal
        self.decimal_return_scale = decimal_return_scale

    def dump(self) -> dict:
        results = super().dump()
        results.update({
            "precision": self.precision,
            "decimal_return_scale": self.decimal_return_scale,
            "asdecimal": self.asdecimal,
        })
        return results


class Binary(BaseField):

    data_type = 'binary'

    def __init__(self, *args, length=None, **kwargs):
        kwargs['length'] = length
        super().__init__(*args, **kwargs)
        self.length = length

    def dump(self) -> dict:
        results = super().dump()
        results.update({
            "length": self.length,
        })
        return results


class Enum(BaseField):

    schema_type = 'string'
    data_type = 'enum'

    def __set_name__(self, owner, name):
        self.enum_name = name

    def __init__(self, *args, enum=None, **kwargs):
        if enum is None:
            enum = []
        kwargs['enum'] = enum
        super().__init__(*args, **kwargs)
        self.enum = enum

    def dump(self) -> dict:
        results = super().dump()
        results.update({
            "enum": self.enum,
        })
        return results


class Key(BaseField):

    data_type = 'key'

    def dump(self) -> dict:
        results = super().dump()
        results["type"] = "big_integer"
        return results


class BigInteger(BaseField):

    data_type = 'big_integer'

    def __init__(self, *args, length=None, **kwargs):
        kwargs['length'] = length
        super().__init__(*args, **kwargs)
        self.length = length

    def dump(self) -> dict:
        results = super().dump()
        results.update({
            "length": self.length,
        })
        return results


class SmallInteger(BigInteger):

    data_type = 'small_integer'

    def __init__(self, *args, length=None, **kwargs):
        kwargs['length'] = length
        super().__init__(*args, **kwargs)
        self.length = length


class Integer(BigInteger):

    data_type = 'integer'

    def __init__(self, *args, length=None, **kwargs):
        kwargs['length'] = length
        super().__init__(*args, **kwargs)
        self.length = length


class String(BaseField):

    data_type = 'string'

    def __init__(self, *args, length=255, **kwargs):
        kwargs['length'] = length
        super().__init__(*args, **kwargs)
        self.length = length

    def dump(self) -> dict:
        results = super().dump()
        results.update({
            "length": self.length,
        })
        return results


class File(BaseField):

    data_type = 'file'
    schema_type = 'string'
    data_format = 'binary'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Date(BaseField):

    data_type = 'date'


class DateTime(BaseField):

    data_type = 'date_time'

    def __init__(self, *args, timezone=None, **kwargs):
        kwargs['timezone'] = timezone
        super().__init__(*args, **kwargs)
        self.timezone = timezone

    def dump(self) -> dict:
        results = super().dump()
        results.update({
            "timezone": self.timezone,
        })
        return results


class Timestamp(DateTime):

    data_type = 'timestamp'

    def __init__(self, *args, timezone=None, **kwargs):
        kwargs['timezone'] = timezone
        super().__init__(*args, **kwargs)
        self.timezone = timezone


class Time(DateTime):

    data_type = 'time'

    def __init__(self, *args, timezone=None, **kwargs):
        kwargs['timezone'] = timezone
        super().__init__(*args, **kwargs)
        self.timezone = timezone


class Text(String):

    data_type = 'string'

    def __init__(self, *args, length=65535, **kwargs):
        kwargs['length'] = length
        super().__init__(*args, **kwargs)
        self.length = length


class Email(String):

    data_type = 'string'
    data_format = 'email'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Phone(String):

    data_type = 'string'
    data_format = "\(?\+[0-9]{1,3}\)? ?-?[0-9]{1,3} ?-?[0-9]{3,5} ?-?[0-9]{4}( ?-?[0-9]{3})? ?(\w{1,10}\s?\d{1,6})?"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

