from functools import wraps
from typing import Callable
import logging

from decorator import decorator
import ujson as json
import boto3

from ion.args import ArgParser

from .items.dashboards import ServiceDashboard
from .utils import print_help, setup_logging

log = logging.getLogger(__name__)


class CliResource:
    @classmethod
    def map_command(cls, command: str) -> Callable:
        if hasattr(cls, command):
            return getattr(cls, command)
        else:
            raise ValueError(f"{cls.__name__} does not support command: '{command}'!")

    @staticmethod
    def get_args():
        return ()

    @staticmethod
    def get_kwargs():
        return {}


class Service(CliResource):
    @staticmethod
    def deploy(service: str, server_type: str, cluster: str, region: str = 'eu-west-1'):
        cloudwatch = boto3.client('cloudwatch', region_name=region)
        response = cloudwatch.put_dashboard(
            DashboardName=service,
            DashboardBody=Service.gen(service, server_type, cluster)
        )
        return response

    @staticmethod
    def get(service: str, server_type: str, cluster: str, **config) -> dict:
        return ServiceDashboard(service, server_type, cluster, **config).generate()

    @staticmethod
    def gen(service: str, server_type: str, cluster: str, **config) -> str:
        return json.dumps(Service.get(service, server_type, cluster, **config))

    @staticmethod
    def show(service: str, server_type: str, cluster: str, **config) -> None:
        print(json.dumps(Service.get(service, server_type, cluster), indent=4))

    @staticmethod
    def get_args():
        args = ArgParser('dash ecs-service <command>')
        service = args.register('service')
        cluster = args.register('cluster')
        server_type = args.register('server-type', short='-st', required=False)
        args.validate()
        return service, server_type or service, cluster



def cli():
    args = ArgParser('dash <resource-name> <command>')
    resource_name = args.register('resource', named=False)
    command = args.register('command', named=False)
    args.validate()
    resource_maker = {'ecs-service': Service}[resource_name]
    cmd_args = resource_maker.get_args()
    if command == 'show':
        print(resource_maker.show(*cmd_args))
    elif command == 'deploy':
        resource_maker.deploy(*cmd_args)
    else:
        print(f'no such command {command!r}')
