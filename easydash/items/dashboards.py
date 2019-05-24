from ion.cache import remember
from .widgets import Widgets
import boto3


class Dashboard:
    def __init__(self, widgets, row_size=6, column_size=6, max_row=24, **kwargs):
        self.params = kwargs
        self.ECS = None
        self.ELBV2 = None
        self.get_resource_name = {
            'LoadBalancer': self.get_load_balancer,
            'TargetGroup': self.get_target_group,
            'ServiceName': self.get_service,
            'ClusterName': self.get_cluster
        }
        self.widget_defs = []
        self.service_name = kwargs['service_name']
        self.server_type = kwargs['server_type']
        x, y = 0, 0
        for widget_def in widgets:
            if widget_def is not None:
                widget, args, kwargs = self.normalize(widget_def)
                widget_object = Widgets.get(widget)
                args = [*args, *self.get_resource_names(widget_object.args)]
                self.widget_defs.append((widget_object, args, dict(kwargs, x=x, y=y)))
            x += row_size
            if x >= max_row:
                x = x % max_row
                y = y + column_size

    @staticmethod
    def normalize(widget_def):
        '''
        Gets widget definition no matter in what form (str, str, and args, etc)
        and returns the full form of this widget's definition
        '''
        if not isinstance(widget_def, tuple):
            return widget_def, (), {}
        if len(widget_def) == 1:
            return widget_def[0], (), {}
        if len(widget_def) == 2:
            if isinstance(widget_def[1], (list, tuple)):
                return widget_def[0], widget_def[1], {}
            return widget_def[0], (), widget_def[1]
        return widget_def

    def get_resource_names(self, types: list) -> list:
        for resource_type in types:
            try:
                yield self.get_resource_name[resource_type]()
            except KeyError as e:
                raise ValueError(f"Could not get a resource type of {resource_type} - please investigate!") from e

    def generate(self, *a, **kw) -> str:
        widgets = [widget.generate(*[*args, *a], **dict(kwargs, **kw)) for widget, args, kwargs in self.widget_defs]
        for widget in widgets:
            widget['properties']['title'] = f"{self.server_type} {widget['properties']['title']}"
        return {'widgets': widgets}

    @remember
    def get_load_balancer(self) -> str:
        if self.ELBV2 is None:
            self.ELBV2 = boto3.client('elbv2')
        res = self.ELBV2.describe_target_groups(TargetGroupArns=[self.get_target_group_arn()])
        return '/'.join(res['TargetGroups'][0]['LoadBalancerArns'][0].split('/')[-3:])

    @remember
    def get_target_group_arn(self) -> str:
        if self.ECS is None:
            self.ECS = boto3.client('ecs')
        res = self.ECS.describe_services(cluster=self.params['cluster_name'], services=[self.service_name])
        target_group_arn = res['services'][0]['loadBalancers'][0]['targetGroupArn']
        return target_group_arn

    @remember
    def get_target_group(self) -> str:
        target_group_name = self.get_target_group_arn().split(':')[-1]
        return target_group_name

    @remember
    def get_service(self) -> str:
        return self.service_name

    @remember
    def get_cluster(self) -> str:
        return self.params['cluster_name']


class ServiceDashboard(Dashboard):
    default_widgets = [
        'ECSCPU',                'ECSMemory',              'ALBRequestCount',           'ALBRequestCountPerTarget',
        'ALBTargetResponseTime', 'ALBTargetSuccessCodes',  'ALBTargetFailedCodes',      'ALBResponseCodes',
        'ALBConsumedLCUs',       'ALBConnections',         'ALBStats',                  'ALBTargetStats',
        'ALBHealthyHostCount'
    ]
    default_widgets = [
        'ECSCPU',                'ECSMemory',                'ALBConnections',                    'ALBHealthyHostCount',
        'ALBRequestCount',       'ALBRequestCountPerTarget', 'ALBRequestCountPerTargetPerSecond', 'ALBTargetResponseTime',
        'ALBTargetStats',        'ALBStats',                 'ALBTargetSuccessCodes',             'ALBResponseCodes',
        None,                    None,                       'ALBTargetFailedCodes'
    ]
    def __init__(self, service_name: str, server_type: str, cluster_name: str) -> None:
        super().__init__(self.default_widgets,
                         service_name=service_name,
                         server_type=server_type,
                         cluster_name=cluster_name)
