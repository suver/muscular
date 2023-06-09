"""Скрипт Setup.py для проекта по упаковке."""

from setuptools import setup, find_packages

import json
import os


def read_pipenv_dependencies(fname):
    """Получаем из Pipfile.lock зависимости по умолчанию."""
    filepath = os.path.join(os.path.dirname(__file__), fname)
    with open(filepath) as lockfile:
        lockjson = json.load(lockfile)
        return [dependency for dependency in lockjson.get('default')]


if __name__ == '__main__':
    setup(
        name='muscles',
        version=os.getenv('PACKAGE_VERSION', '0.0.1'),
        description='Py Framework.',
        license='MIT',
        author='Denis Butko',
        author_email='denis@butko.info',
        package_dir={'': 'src'},
        url='http://freamwork.muscles.space',
        packages=find_packages('src', include=[
            '*'
        ]),
        install_requires=[
            *read_pipenv_dependencies('Pipfile.lock'),
        ]
    )
