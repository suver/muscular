# Схемы

Главная идея фреймворка это общая схема, 
которая подходить как для DTO или генерации swagger документации, 
так и для
настройки роутов, 
адресных консольных команд и много другого.

## Генерация DTO

Родительские модели:

`Collection(collection_name, *columns)` - формирование коллекции, где 

- `collection_name` - название коллекции,
- `*columns` - набор полей

или

`Model` - базовый объект для формирование модели DTO

### Пример: Collection
```python
from muscles import String
from muscles import Column
from muscles import Key
from muscles import Collection

r = Collection("user",
                   Column("id", 
Key),
                   Column("name", 
String, 
index=True),
                   Column("family", 
String, 
index=True)
               )
print(r.dump())

""" result >
{
    'class': 'Collection',
    'children': [
        {
            'id': {
                'class': 'Key',
                'children': [],
                'data_type': 'key',
                'type': 'big_integer',
                'format': None,
                'index': False,
                'unique': False,
                'default': None,
                'required': False,
                'title': None,
                'description': None,
                'nullable': True,
                'value': None,
                'primary_key': False,
                'example': None,
                'error': None
            }
        },
        {
            'name': {
                'class': 'String',
                'children': [],
                'data_type': 'string',
                'type': 'string',
                'format': None,
                'length': 255,
                'index': True,
                'unique': False,
                'default': None,
                'required': False,
                'title': None,
                'description': None,
                'nullable': True,
                'value': None,
                'primary_key': False,
                'example': None,
                'error': None
            }
        },
        {
            'family': {
                'class': 'String',
                'children': [],
                'data_type': 'string',
                'type': 'string',
                'format': None,
                'length': 255,
                'index': True,
                'unique': False,
                'default': None,
                'required': False,
                'title': None,
                'description': None,
                'nullable': True,
                'value': None,
                'primary_key': False,
                'example': None,
                'error': None
            }
        }
    ]
}
"""
```


### Пример: Model
```python
from muscles import String
from muscles import Column
from muscles import Key
from muscles import Enum
from muscles import Date
from muscles import DateTime
from muscles import Model

class User(Model):
    id = Column(Key)
    name = Column(String, index=True)
    email = Column(String, index=True)
    status = Column(Enum(enum=['inactive', 'deleted', 'blocked', 'active']), index=True)
    birthday = Column(Date)
    created_at = Column(DateTime)

# Создаем объект DTO с заранее занесенными данными    
u = User(name="test name", status="blocked")

# Обновляем поле новым значением
u.email = 'mmm@mail.ru'

print(u.dump())

""" result >
{
    'User': {
        'type': 'object', 
        'properties': {
            'id': {
                'class': 'Key', 
                'children': [], 
                'data_type': 'key', 
                'type': 'big_integer', 
                'format': None, 
                'index': False, 
                'unique': False, 
                'default': None, 
                'required': False, 
                'title': None, 
                'description': None, 
                'nullable': True, 
                'value': None, 
                'primary_key': False, 
                'example': None, 
                'error': None
            }, 
            'name': {
                'class': 'String', 
                'children': [], 
                'data_type': 'string', 
                'type': 'string', 
                'format': None, 
                'length': 255, 
                'index': True, 
                'unique': False, 
                'default': None, 
                'required': False, 
                'title': None, 
                'description': None, 
                'nullable': True, 
                'value': 'test name', 
                'primary_key': False, 
                'example': None, 
                'error': None
            }, 
            'email': {
                'class': 'String', 
                'children': [], 
                'data_type': 'string', 
                'type': 'string', 
                'format': None, 
                'length': 255, 
                'index': True, 
                'unique': False, 
                'default': None, 
                'required': False, 
                'title': None, 
                'description': None, 
                'nullable': True, 
                'value': 'mmm@mail.ru', 
                'primary_key': False, 
                'example': None, 
                'error': None
            }, 
            'status': {
                'class': 'Enum', 
                'children': [], 
                'data_type': 'enum', 
                'type': 'string', 
                'format': None, 
                'enum': [
                    'inactive', 
                    'deleted', 
                    'blocked', 
                    'active'
                ], 
                'index': True, 
                'unique': False, 
                'default': None, 
                'required': False, 
                'title': None, 
                'description': None, 
                'nullable': True, 
                'value': 'blocked', 
                'primary_key': False, 
                'example': None, 
                'error': None
            }, 
            'birthday': {
                'class': 'Date', 
                'children': [], 
                'data_type': 'date', 
                'type': 'date', 
                'format': None, 
                'index': False, 
                'unique': False, 
                'default': None, 
                'required': False, 
                'title': None, 
                'description': None, 
                'nullable': True, 
                'value': None, 
                'primary_key': False, 
                'example': None, 
                'error': None
            }, 
            'created_at': {
                'class': 'DateTime', 
                'children': [], 
                'data_type': 'date_time', 
                'type': 'date_time', 
                'format': None, 
                'timezone': None, 
                'index': False, 
                'unique': False, 
                'default': None, 
                'required': False, 
                'title': None, 
                'description': None, 
                'nullable': True, 
                'value': None, 
                'primary_key': False, 
                'example': None, 
                'error': None
            }
        }
    }
}
"""
```

## Значение Column

`Column` - Определяет объект значения/поля модели. Определяет тип, валидаторы и формат возможных значений

Используется в формате `Column(<ТипПоля>, **Аргументы)`

### Пример: Column
```python
class Test(Model):
    name = Column(String, index=True)

# или отдельно, но в этом случае требуется первым аргументом указать название поля, а вторым уже тип   
c = Column("name", String)
```

Аргументы:

- `index` = Указывает на то что значение используется как индекс. Значение по умолчанию: `False`. 
- `unique` = Уникальное значение. Значение по умолчанию: `False`. 
- `primary_key` = Тип PK. Значение по умолчанию: `False`.
- `nullable` = Значение может быть пустым (`None`). Значение по умолчанию: `True`. 
- `default` = Значение по умолчанию. Значение по умолчанию: `None`.
- `required` = Обязательно для заполнения. Значение по умолчанию: `False`.
- `title` = Заголовок поля. Значение по умолчанию: `None` 
- `description` = Описание поля. Значение по умолчанию: `None` 
- `example` = Пример заполнения. Используется в swagger схемах и других местах. Значение по умолчанию: `None` 
- `min_length` = Минимальное кол-во символом/минимальная цифра/минимальное кол-во элементов. Значение по умолчанию: `None` 
- `max_length` = Максимальное кол-во символом/максимальная цифра/максимальное кол-во элементов. Значение по умолчанию: `None`


Типы поля: 

- `Boolean` - Булевое значение
- `Key` - Указывает на ключ
- `String` - Строка
- `Enum` - Выбор. Пример: `Column(Enum(enum=['inactive', 'deleted', 'blocked', 'active']), index=True)`
- `Email` - Формат данных соответствует формату email
- `DateTime` - Дата и Время
- `Float` - Число с точкой
- `List` - Массив/Список
- `Binary` - Бинарное значение, например файл
- `UUID4` - Формат соответсвует UUID v4
- `BigInteger` - Цифра
- `SmallInteger` - Цифра от -5 до 256
- `Integer` - Цифра
- `Json` - Формат JSON
- `File` - Бинарный файл
- `Date` - Дата
- `Timestamp` -  Timestamp
- `Time` - Время
- `Text` - Текст без ограничений
- `Numeric` - Цифра в любом типе (int, float, string, dabble .etc)
- `Phone` - Формат данных соответствует формату номера телефона


### Пример: Column
```python
from muscles import Model
from muscles import Column
from muscles import Boolean
from muscles import Key
from muscles import String
from muscles import Enum
from muscles import Email
from muscles import DateTime
from muscles import Float
from muscles import List
from muscles import Binary
from muscles import UUID4
from muscles import BigInteger
from muscles import SmallInteger
from muscles import Integer
from muscles import Json
from muscles import File
from muscles import Date
from muscles import Timestamp
from muscles import Time
from muscles import Text
from muscles import Numeric
from muscles import Phone

# Column можно использовать как свойство класса
class User(Model):
    id = Column(Key)
    name = Column(String, index=True)
    email = Column(String, index=True)
    status = Column(Enum(enum=['inactive', 'deleted', 'blocked', 'active']), index=True)
    birthday = Column(Date)
    created_at = Column(DateTime)

u = User()

# или отдельно, но в этом случае требуется первым аргументом указать название поля, а вторым уже тип   
c = Column("test", Boolean)
```


## Parameter

- `FormParameter` - Параметры, которые передаются в формах.
- `HeaderParameter` - Параметры, которые передаются в заголовках.
- `QueryParameter` - Параметры, которые передаются в части query стандартного URL.
- `CookieParameter` - Параметры, которые передаются в куках.
- `PathParameter` - Параметры, которые передаются в секции path стандартного URL.

Пример: 

`QueryParameter('ключ_параметра', <ТипПоля>, required=False/True, description='Описание')`

`QueryParameter('query2', Enum(enum=['one', 'two']), required=False, description='Query2')`

Аргументы:

- `explode` - (True/False) указывает, должны ли массивы и объекты генерировать отдельные параметры для каждого 
элемента массива или свойства объекта.
- `required` - (True/False) обязательный параметр или нет
- `description` - (String) описание параметра



### Пример: PathParameter
```python
from muscles import PathParameter
from muscles import Numeric

r = PathParameter('id', Numeric, required=True, description='Path ID')
print(r.dump())
# >
"""
{
    'required': True,
    'explode': False,
    'description': 'Path ID',
    'name': 'id',
    'schema': {
        'class': 'Numeric',
        'children': [],
        'data_type': 'number',
        'type': 'number',
        'format': '^\\d+$',
        'precision': None,
        'scale': None,
        'decimal_return_scale': None,
        'asdecimal': True
    },
    'in': 'path'
}
"""
```


## Request


- `RequestBody` - Базовый объект модели RequestBody. Часть схемы отвечающей за получение запроса. Объект `RequestBody`
    содержит дополнительный аргумент `content_type`, указывающий тип контента.
- `FileRequestBody` - Определяет формат JSON текущего запроса. Объект `FileRequestBody`
    содержит дополнительный аргумент `content_type`, указывающий тип контента.
- `JsonRequestBody` - Определяет формат application/json текущего запроса
- `XmlRequestBody` - Определяет формат application/xml текущего запроса
- `FormRequestBody` - Определяет формат application/x-www-form-urlencoded текущего запроса
- `MultipartRequestBody` - Определяет формат multipart/form-data текущего запроса
- `PayloadRequestBody` - Определяет формат text/plain текущего запроса
- `TextRequestBody` - Определяет формат text/plain текущего запроса

Аргументы:

`content_type` - указывающий тип контента, например application/json. Значение по умолчанию: `None`
`description` - описание. Значение по умолчанию: `None`
`model` - DTO модель данных, если данные передаются заранее оговоренном формате. Значение по умолчанию: `None`
`is_list` - если True, указывает на то что передается список значений/моделей. Значение по умолчанию: `False`
`min_items` - минимальное кол-во значений (для списка). Значение по умолчанию: `0`
`max_items` - максимальное кол-во значений (для списка). Значение по умолчанию: `0`
`unique_items` - если True то каждый элемент списка должен быть уникальный. Значение по умолчанию: `False`

### Пример
```python
from muscles import JsonRequestBody
from muscles import String

r = JsonRequestBody(description='Json', model=String, is_list=True, max_items=10, min_items=1)
r.dump()
""" result >
{
    'application/json': {
        'description': 'Json',
        'schema': {
            'type': 'array',
            'items': {
                'class': 'String',
                'children': [],
                'data_type': 'string',
                'type': 'string',
                'format': None,
                'length': 255
            },
            'minItems': 1,
            'maxItems': 10
        }
    }
}
"""
```


## Response

Формирует схему ответа на запрос


- `ResponseBody` - Ответ в формате соответсвующем значениею аргумента content_type.
- `HtmlResponseBody` - Ответ в формате text/html
- `JsonResponseBody` - Ответ в формате application/json
- `XmlResponseBody` - Ответ в формате application/xml
- `TextResponseBody` -Ответ в формате text/plain

Аргументы:

`content_type` - Content-Type. Значение по умолчанию: `None`.
`description` - Описание. Значение по умолчанию: `None`.
`http_code` - HTTP код ответа. Значение по умолчанию: `None`.
`model` - Объект DTO дляуказания формата ответа. Значение по умолчанию: `None`.
`is_list` - Если True то ответ является списком. Значение по умолчанию: `False`.
`min_items` - Минимальное значение списка. Значение по умолчанию: `0`.
`max_items` - Максимальное значение списка. Значение по умолчанию: `0`.
`unique_items` - Каждое значение списка уникально. Значение по умолчанию: `False`.
`base_schema` - Базовая схема. Указывается как объект, унаследованный от `Response`. Значение по умолчанию: `None`.

### Пример
```python
from muscles import Model
from muscles import Column
from muscles import Key
from muscles import ResponseBody
from muscles import TextResponseBody

r = ResponseBody(description='OK', content_type='application/pdf')
r.dump()

""" result >
{
    'application/pdf': {
        'http_code': None,
        'content_type': 'application/pdf',
        'description': 'OK',
        'schema': None
    }
}
"""

class SchTest(Model):
    id = Column(Key)
    
r = TextResponseBody(http_code=200, model=SchTest)
r.dump()

""" result >
{
    'text/plain': {
        'http_code': 200,
        'content_type': 'text/plain',
        'description': None,
        'schema': {
            '$ref': '#/components/schemas/SchTest'
        }
    }
}
""""
```


## Security

Объект указывающий схему авторизации

-`BaseSecurity` - Базовый объект схемы авторизации/аутентификации.
-`BasicAuthSecurity` - Basic авторизация.
-`ApiKeyAuthSecurity` - HTTP key авторизация.
-`BearerAuthSecurity` - Bearer / JWT авторизация.

Аргументы: каждый из объектов содержит схожие аргументы, но они уже предзаполнены по умолчанию.

### Пример
```python
from muscles import ApiKeyAuthSecurity

r = ApiKeyAuthSecurity()
assert r.dump() == {
    'ApiKeyAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Api-Token'
    }
}
```


## Swagger

Коллекция схемы Swagger/OpenApi3. Данная схема объединяет все предыдущие схемы и формирует схему, 
пригодную для использования в Swagger. Ниже представлены два возможных варианта заполнения схемы.


### Пример
```python
from muscles import Model
from muscles import Column
from muscles import Key
from muscles import Swagger
from muscles import QueryParameter
from muscles import Enum
from muscles import String
from muscles import ApiKeyAuthSecurity
from muscles import JsonResponseBody
from muscles import XmlResponseBody
from muscles import TextRequestBody


class SchTest(Model):
    id = Column(Key)

r = Swagger(
    title="Test",
    name="Test 2",
    version="1.2",
    description="Test Swagger Api",
    termsOfService="https://terms",
    servers=[{"url": "/api/v1"}],
    contact_email="admin@mail.ru",
    request=TextRequestBody(description='Form', model=String, is_list=True),
    parameters=QueryParameter('query2', Enum(enum=['one', 'two']), required=False, description='Query2'),
    security=[
        ApiKeyAuthSecurity()
    ],
    response=JsonResponseBody(description='OK', model=SchTest)
)
assert r.dump() == {
    'info': {
        'title': 'Test',
        'version': '1.2'
    },
    'openapi': '3.0.3',
    'description': 'Test Swagger Api',
    'termsOfService': 'https://terms',
    'servers': [{'url': '/api/v1'}],
    'contact': {'email': 'admin@mail.ru'},
    'request': {
        'text/plain': {
            'description': 'Form',
            'schema': {
                'type': 'array',
                'items': {
                    'class': 'String',
                    'children': [],
                    'data_type': 'string',
                    'type': 'string',
                    'format': None,
                    'length': 255
                }
            }
        }
    },
    'response': {
        'application/json': {
            'http_code': None,
            'content_type': 'application/json',
            'description': 'OK',
            'schema': {'$ref': '#/components/schemas/SchTest'}
        }
    },
    'parameters': {
        'required': False,
        'explode': False,
        'description': 'Query2',
        'name': 'query2',
        'schema': {
            'class': 'Enum',
            'children': [],
            'data_type': 'enum',
            'type': 'string',
            'format': None,
            'enum': ['one', 'two']
        },
        'in': 'query'
    },
    'components': {
        'securitySchemes': {
            'ApiKeyAuth': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'X-Api-Token'
            }
        }
    }
}
```

### Пример
```python
from muscles import Model
from muscles import Column
from muscles import Key
from muscles import Swagger
from muscles import QueryParameter
from muscles import Enum
from muscles import String
from muscles import ApiKeyAuthSecurity
from muscles import JsonResponseBody
from muscles import XmlResponseBody
from muscles import TextRequestBody


class SchTest(Model):
    id = Column(Key)

r = Swagger(
    title="Test",
    name="Test 2",
    version="1.2",
    description="Test Swagger Api",
    termsOfService="https://terms",
    servers=[{"url": "/api/v1"}],
    contact_email="admin@mail.ru",
    request=[
        TextRequestBody(description='Form', model=String, is_list=True),
    ],
    parameters=[
        QueryParameter('query2', Enum(enum=['one', 'two']), required=False, description='Query2'),
    ],
    security=[
        ApiKeyAuthSecurity()
    ],
    response={
        200: [
            JsonResponseBody(description='OK', model=SchTest),
            XmlResponseBody(description='OK', model=SchTest),
        ],
        404: JsonResponseBody(description='NOT FOUND', model=SchTest),
    }
)
assert r.dump() == {
    'info': {
        'title': 'Test',
        'version': '1.2'
    },
    'openapi': '3.0.3',
    'description': 'Test Swagger Api',
    'termsOfService': 'https://terms',
    'servers': [{'url': '/api/v1'}],
    'contact': {'email': 'admin@mail.ru'},
    'request': [
        {
            'text/plain': {
                'description': 'Form',
                'schema': {
                    'type': 'array',
                    'items': {
                        'class': 'String',
                        'children': [],
                        'data_type': 'string',
                        'type': 'string',
                        'format': None,
                        'length': 255
                    }
                }
            }
        }
    ],
    'response': {
        200: [
            {
                'application/json': {
                    'http_code': None,
                    'content_type': 'application/json',
                    'description': 'OK',
                    'schema': {'$ref': '#/components/schemas/SchTest'}
                }
            },
            {
                'application/xml': {
                    'http_code': None,
                    'content_type': 'application/xml',
                    'description': 'OK',
                    'schema': {'$ref': '#/components/schemas/SchTest'}
                }
            }
        ],
        404: {
            'application/json': {
                'http_code': None,
                'content_type': 'application/json',
                'description': 'NOT FOUND',
                'schema': {
                    '$ref': '#/components/schemas/SchTest'
                }
            }
        }
    },
    'parameters': [
        {
            'required': False,
            'explode': False,
            'description': 'Query2',
            'name': 'query2',
            'schema': {
                'class': 'Enum',
                'children': [],
                'data_type': 'enum',
                'type': 'string',
                'format': None,
                'enum': ['one', 'two']
            },
            'in': 'query'
        }
    ],
    'components': {
        'securitySchemes': {
            'ApiKeyAuth': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'X-Api-Token'
            }
        }
    }
}
```