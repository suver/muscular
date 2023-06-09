from .schema import Schema


class BaseColumn(Schema):

    def __set_name__(self, owner, name):
        self.column_name = name
        if not hasattr(owner, 'columns'):
            setattr(owner, 'columns', dict())
        owner.columns[name] = self

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(args) > 1:
            self.column_name = args[0]
            self.field_type = args[1] if not callable(args[1]) else args[1]()
        elif len(args) == 1:
            self.field_type = args[0] if not callable(args[0]) else args[0]()

    def __set__(self, instance, value):
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def dump(self) -> dict:
        return {
            self.column_name: self.field_type.dump()
        }

    def to_json(self) -> dict:
        return {
            self.column_name: self.field_type.getstate(self.value)
        }


class Column(BaseColumn):

    def __init__(self, *args, index=False, unique=False, primary_key=False, nullable=False, default=None,
                 required=False, title=None, description=None, example=None, **kwargs):
        super().__init__(*args, index=index, unique=unique, primary_key=primary_key, nullable=nullable, default=default,
                 required=required, title=title, description=description, example=example, **kwargs)
        kwargs['index'] = index
        kwargs['unique'] = unique
        kwargs['primary_key'] = primary_key
        kwargs['nullable'] = nullable
        kwargs['default'] = default
        kwargs['required'] = required
        kwargs['title'] = title
        kwargs['description'] = description
        kwargs['example'] = example
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

    def dump(self) -> dict:
        results = super().dump()
        results[self.column_name].update({
            "index": self.index,
            "unique": self.unique,
            "default": self.default,
            "required": self.required,
            "title": self.title,
            "description": self.description,
            "nullable": self.nullable,
            "value": self.default,
            "primary_key": self.primary_key,
            "example": self.example,
        })
        return results
