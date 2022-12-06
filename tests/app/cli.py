from muscles import CliStrategy, cli
from .instance import Muscular


muscular = Muscular()
muscular.context.strategy = CliStrategy


@cli.group()
def db(*args):
    return 'db'


@db.command(command_name='migrate')
def db_migrate(*args):
    return 'db migrate'


@db.group(command_name='dbf')
def dba(*args):
    pass


@dba.command()
def dbaa(*args):
    return 'dbaa'


@cli.command(command_name='prompt')
@cli.argument('--user', short='-u', description='User login', prompt='Enter user login')
@cli.argument('--password', short='-p', description='User password', prompt='Enter user password', password=True)
@cli.argument('--email', short='-e', description='User email', prompt='Enter user email', nargs=2)
def stest_prompt(*args, user, password, email):
    ''' Test function for command '''
    return [user, password, email]


@cli.command(command_name='test')
@cli.argument('--test', short='-t', description='Test system', required=True, default=False)
@cli.argument('--check', short='-c', description='Check system', default=0, flag_value=1, dest='chunk')
@cli.argument('--prompt', short='-p', description='Prompt system', prompt="Enter Prompt")
@cli.argument('--list', short='-l', description='List system', prompt="List Prompt", nargs=4)
@cli.argument('--value', short='-v', description='Value system', nargs=1, required=False)
@cli.argument('--multiple', short='-m', description='multiple system', nargs=1, multiple=True)
@cli.argument('--password', short='-w', description='Password system', nargs=1, required=False, password=True,
              prompt='Password')
@cli.flag('-u', description='U system')
def stest_command2(arg, test, chunk, u, prompt, list, value, password, multiple):
    ''' Test Muscular failed, variables contain different instances Test Muscular failed, variables contain
    different instances Test Muscular failed, variables contain different instances Test Muscular failed,
    variables contain different instances '''
    return [test, chunk, u, prompt, list, value, password, multiple]

