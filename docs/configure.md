# Пример работы с конфигурацией


-  `!environ` - Вставляет значение из переменной окружения. Пример: `!environ FLASK_ENV` или если значение не указано, то подставляется по умолчанию. Пример: `!environ FLASK_ENV or production`
-  `!basedir` - Вставляет значение рутовой директории проекта. Пример: `!basedir`
-  `!include_dir` - Подключает все файлы в директории. Пример: `!include_dir ./config/modules`
-  `!include` - Подключает файл указанный в пути. Пример: `!include ./config/acl.yaml`
-  `!basepath` - Вставляет к basedir следующие диретории. Пример: `!basepath storage > /www/storage`
-  `!secret` - Вставляет значение из файла секрет и константой определенной следующим параметром. Пример: `!secret SENTRY_IO_KEY`



## Пример файлов конфигураций


#### file: configuration.yaml
```yaml
main:
  basedir: !basedir
  base_url: !environ BASE_URL or localhost:5000
  server_name: !environ SERVER_NAME or localhost:5000
  host: !environ HOST or localhost
  port: !environ PORT or 8080
  env: !environ FLASK_ENV or production
  debug: !environ DEBUG or False
  timezone: UTC
  main_route: page.index
  locale_mode: cookie # url, cookie - переключение языка

  languages:
    en:
      name: English
      icon: /static/media/svg/flags/en.svg
    ru:
      name: Русский
      icon: /static/media/svg/flags/ru.svg
    en_US:
      name: Unaited State
      icon: /static/media/svg/flags/us.svg

  default_language: en

  secret_key: !environ SECRET_KEY or dhU73jslvbglsjg&20lfjsl
  csrf_enabled: False


acl: !include ./config/acl.yaml


params:
  ContactMail: support@twonerds.xyz

authorization:
  bearer:
    - key: sDJ72344sdF5435dsfgpeiv2534ndj4HkdUfsj4
      name: Core
      roles:
        - root

modules: !include_dir ./config/modules


middlewares:
  - package: app.middleware.example
  - package: app.middleware.authorization
    user:
      class: User
      package: app.modules.user.models

schemas:

```


#### file: acl.yaml
```yaml
api:
  permission: nobody
```


#### file: secret.yaml
```yaml
SENTRY_IO_KEY: https://234234234@sentry.io/1725642
SQLALCHEMY_DATABASE_URI: !environ SQLALCHEMY_DATABASE_URI or mysql://root:root@localhost/simple
RABBITMQ_URL: !environ RABBITMQ_URL or amqp://guest:guest@rabbitmq:5672/%2F
```


#### file: sensors.yaml
```yaml
  - sensor 1
  - sensor 2

```


#### file: modules/example.yaml
```yaml
example:
  package: app.modules.example
  name: Example
  static_folder: /static/main
  sensor: !include ./config/sensors.yaml

```


#### file: modules/page.yaml
```yaml
page:
  package: app.modules.page
  name: Page
  static_folder: /static/page

```


#### file: modules/storage.yaml
```yaml
storage:
  package: app.modules.storage
  name: Storage
  static_folder: /static/storage
  upload_url: ./storage
  upload_folder: !basepath storage

```


## Пример работы с конфигурацией


### Настройки через файл конфигурации
```python
import os
from muscles import Configurator

directory = os.path.dirname(os.path.abspath(__file__))
config = Configurator(file='./config/configuration.yaml', basedir=directory)

# Способы получить занчение из конфигурации
config.modules.example.package.value() # > app.modules.example
config.acl.api.permission.value() # > nobody
str(config.acl.api.permission) # > nobody
str(config.acl.get('api.permission')) # > nobody
dict(config.acl) # > {'api': {'permission': 'nobody'}}
repr(config.acl.api) # > Configurator(permission: nobody\n)
```


### Настройка через объект конфигурации
```python
import os
from muscles import Configurator

directory = os.path.dirname(os.path.abspath(__file__))
config = Configurator(obj={
        "main": {
            "BASEDIR": ".",
            "BASE_URL": "localhost: 5050",
            "SERVER_NAME": "localhost: 5050",
            "HOST": "localhost",
            "PORT": "5050",
            "ENV": "production",
            "DEBUG": False,
            "TIMEZONE": "UTC",
            "MAIN_ROUTE": "page.index",
            "SQLALCHEMY_DATABASE_URI": "SQLALCHEMY_DATABASE_URI",
            "SQLALCHEMY_TRACK_MODIFICATIONS": True,
            "SQLALCHEMY_ON": True,
            "PROJECT_ROOT": ".",
            "STATICFILES_DIRS": "static",
            "SESSION_KEY_PREFIX": "session",
            "SESSION_TYPE": "filesystem",
            "SECRET_KEY": "dhU73jslvbglsjg&20lfjsl",
        },
        "routes": {
            "prefix": '',
        },
        "api": {
            "prefix": "/api",
            "default_version": "v1",
            "controllers": {
                "Test": "controllers.test",
                "TestRequest": "controllers.request",
            }
        }
    }, basedir=directory)

```

**ВНИМАНИЕ:** Одновременно можно использовать конфигурацию либо через файл, либо через объект