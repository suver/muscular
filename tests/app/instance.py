import os
import sys
from muscles import WsgiStrategy
from muscles import RestApi
from muscles import Context, MuscularSingletonMeta
from muscles import Configurator

directory = os.path.dirname(__file__)
sys.path.append(f"{directory}")
sys.path.append(os.path.abspath(f"{directory}/.."))
sys.path.append(os.path.abspath(f"{directory}/../.."))


class Muscular(metaclass=MuscularSingletonMeta):
    package_paths = []
    shutup = True

    config_file = './config/configuration.yaml'

    config = Configurator(file=os.path.join(os.path.dirname(__file__), config_file), basedir=os.path.dirname(__file__))

    context = Context(WsgiStrategy, {})

    def __init__(self):
        self.api1 = RestApi(
            prefix='/api/v1',
            version='1.0',
            name='ApiV1',
            title='Api v1',
            description='Системный Api',
            termsOfService='http://swagger.io/terms/',
            contact_email='**@**.info',
        )

        self.init_auto_packages(self.config)
        self.init_imports(self.config.models)
        self.init_imports(self.config.api.controllers)

    @context.before_start()
    def before_start(self_context):
        # print('>>>>>>>>>>>>before_start')
        pass

    @context.after_start()
    def after_start(self_context, result):
        # print('>>>>>>>>>>>>after_start', result)
        pass

    def run(self, *args):
        return self.context.execute(*args, shutup=self.shutup)

    def __call__(self, environ, start_response):
        self.context.set_param('environ', environ)
        self.context.set_param('start_response', start_response)
        return self.context.execute()


muscular = Muscular()
