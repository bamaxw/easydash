from .items.dashboards import ServiceDashboard
from typing import Callable
import boto3
import json


class CliResponse:
    @classmethod
    def map_command(cls, command: str) -> Callable:
        if hasattr(cls, command):
            return getattr(cls, command)
        else:
            raise ValueError(f"{cls.__name__} does not support command: '{command}'!")

class Service:
    @staticmethod
    def deploy(service: str, server_type: str, cluster: str, region: str='eu-west-1'):
        cloudwatch = boto3.client('cloudwatch', region_name=region)
        response = cloudwatch.put_dashboard(
            DashboardName=service,
            DashboardBody=Service.gen(service, cluster)
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


map_resource = {
    'ecs-service': Service
}
