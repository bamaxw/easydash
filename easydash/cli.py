'''EasyDash command line utilities'''
from functools import wraps
import logging

from decorator import decorator
import click
import json

# from .items.dashboards import ServiceDashboard
from .utils import with_options, print_help, setup_logging
from .mock import Dashboard
from .config import CONFIG
from . import defaults

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@click.group()
def cli():
    '''EasyDash command line client'''
    pass

def base_cmd(cmd):
    @wraps(cmd)
    @click.argument('bundles', required=False, nargs=-1)
    @click.option('file', '--file', '-f', type=click.File('r'))
    @click.option('verbose', '-v', '--verbose', count=True)
    def _wrapper(bundles, file, verbose, **options):
        logger.debug(f'Received arguments:\n{options}')
        setup_logging(verbose)
        if not bundles and file is None:
            print(cmd)
            print_help(cmd)
            raise SystemExit(f"Please provide either bundle name or config --file!")
        if file:
            config = json.load(file)
            return cmd(dict(options, **config))
        return cmd(bundles=bundles, **options)
    return _wrapper

@cli.command('show')
# @with_options(defaults.OPTIONS)
@base_cmd
@click.pass_context
def show(ctx, bundles, **options):
    '''Show CloudWatch dashboard config without deploying it'''
    dashboard_command = Dashboard.get(bundles).show
    ctx.forward(dashboard_command)
    ctx.invoke(dashboard_command, **options)
