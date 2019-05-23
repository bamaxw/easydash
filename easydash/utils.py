'''EasyDash command line utilities'''
from functools import wraps
import logging

from decorator import decorator
import click

from . import defaults

logger = logging.getLogger(__name__)
LOGLEVELS = [logging.getLevelName(defaults.LOGLEVEL), logging.WARNING, logging.INFO, logging.DEBUG]


def print_help(command):
    '''Print help for click command'''
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))

def setup_logging(verbose: int):
    '''
        Set logging log-level to specified value
        Args:
            - verbose: number for 0 to 3 specifying how verbose should the logger be
    '''
    level: int = LOGLEVELS[verbose]
    logging.basicConfig(level=level)

def normalize_args_kwargs(arg_kwarg):
    '''
        Receive any object and convert it to tuple and dict
        so that it can be passed into a function call
        Examples:
            >>>normalize_args_kwargs('max')
            ('max',), {}
            >>>normalize_args_kwargs(('max',))
            ('max',), {}
            >>>normalize_args_kwargs(('python', 'max', {'required': False}))
            ('python', 'max'), {'required': False}
    '''
    if isinstance(arg_kwarg, (list, tuple)):
        if isinstance(arg_kwarg[-1], dict):
            args = arg_kwarg[:-1]
            kwargs = arg_kwarg[-1]
        else:
            args = arg_kwarg
            kwargs = {}
    else:
        args = (arg_kwarg,)
        kwargs = {}
    logger.debug(f'Config {arg_kwarg} split into args: {args} and kwargs: {kwargs}')
    return args, kwargs

def printargs(func):
    @wraps(func)
    def _wrapper(*a, **kw):
        print('Function:', func, '\nPrintargs:\n', '\n'.join(str(arg) for arg in a))
        if kw:
            print(kw)
        return func(*a, **kw)
    return _wrapper

@printargs
def with_options(opt_definitions=()):
    '''Decorates command with click options and arguments'''
    def _wrap_with_options(cmd):
        for opt_definition in opt_definitions:
            logger.debug('option:' + str(opt_definition))
            args, kwargs = normalize_args_kwargs(opt_definition)
            cmd = wraps(cmd)(click.option(*args, **kwargs)(cmd))
        return cmd
    return _wrap_with_options
