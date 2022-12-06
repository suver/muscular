import io
from contextlib import redirect_stdout
from ..app.cli import muscular


def test_1():
    f = io.StringIO()
    with redirect_stdout(f):
        muscular.shutup = False
        result = muscular.run('help')
    s = f.getvalue()
    assert len(s) > 500


def test_2():
    f = io.StringIO()
    with redirect_stdout(f):
        muscular.shutup = True
        result = muscular.run('db')
    assert result == 'db'


def test_3():
    f = io.StringIO()
    with redirect_stdout(f):
        muscular.shutup = True
        result = muscular.run('db', 'migrate')
    assert result == 'db migrate'


def test_4():
    f = io.StringIO()
    with redirect_stdout(f):
        muscular.shutup = True
        result = muscular.run('db', 'dbf', 'dbaa')
    assert result == 'dbaa'


def test_5():
    f = io.StringIO()
    with redirect_stdout(f):
        muscular.shutup = True
        result = muscular.run('prompt', '-u', 'user', '-p', 'password', '--email', 'email1', 'email2')
    assert result == ['user', 'password', ['email1', 'email2']]


def test_6():
    f = io.StringIO()
    with redirect_stdout(f):
        muscular.shutup = True
        result = muscular.run('test', '-t', '-u', '-c', '--multiple', '--password', 'ddd', '-p', 'pr',
                              '-l', '1', '2', '3', '4', '-v', 'w', '-m', 'f')
    assert result == [True, 1, True, 'pr', ['1', '2', '3', '4'], 'w', 'ddd', ['f']]
