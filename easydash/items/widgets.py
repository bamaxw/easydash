from ..config import config, section_by_namespace
from helpers.list import as_list
import json


class Widgets:
    widgets = {}

    @classmethod
    def __str__(cls) -> str:
        return str(cls.widgets)

    @classmethod
    def __repr__(cls) -> str:
        return json.dumps({key: str(value) for key, value in cls.widgets.items()}, indent=4)

    @classmethod
    def add(cls, widget):
        cls.widgets[widget.qualname] = widget

    @classmethod
    def get(cls, qualname):
        try:
            return cls.widgets[qualname]
        except KeyError:
            raise KeyError(f"Widget with name {qualname} does not exist! Choose from the list: {list(cls.widgets.keys())}")

    @classmethod
    def generate(cls, qualname, resource_name, **kw):
        return cls.get(qualname).generate(resource_name, **kw)


class Widget:
    def __init__(self, section, namespace, resource_type, properties_conf):
        if type(properties_conf) is str:
            self.type = 'metric'
            self.qualname = f'{section}{properties_conf}'
        else:
            self.type = properties_conf.get('type', 'metric')
            self.qualname = f'{section}{properties_conf["name"]}'
        self.properties = Properties(namespace, resource_type, properties_conf)
        self.args = as_list(resource_type)
        Widgets.add(self)

    def __str__(self) -> str:
        return f'<{self.qualname}Widget>'

    def __repr__(self) -> str:
        return str(self)

    def generate(self, *resource_names, type=None, x=0, y=0, width=6, height=6, **kw):
        if len(resource_names) != len(self.args):
            raise ValueError(f'Must provide arguments: {self.args} to {self.qualname}!')
        if type is None:
            type = self.type
        return {
            'x': x,
            'y': y,
            'type': type,
            'width': width,
            'height': height,
            'properties': self.properties.generate(*resource_names, **kw)
        }


class Properties:
    def __init__(self, namespace, resource_type, conf):
        if type(conf) is str:
            conf = {'name': conf, 'metrics': [conf]}
        if 'metrics' not in conf:
            conf['metrics'] = [conf['name']]
        self.view = conf.pop('view', 'timeSeries')
        self.stacked = conf.pop('stacked', False)
        self.region = conf.pop('region', 'eu-west-1')
        self.period = conf.pop('period', 300)
        self.name = conf.pop('name')
        self.title = conf.pop('title', self.make_title(self.name))
        self.metrics = Metrics(namespace, resource_type, conf)

    def make_title(self, name):
        return ''.join(self._make_title(name))

    def _make_title(self, name):
        for i, char in enumerate(name):
            if i == 0:
                yield char
                continue
            if i == len(name):
                yield char
                continue
            if char.upper() == char:
                if name[i-1].upper() != name[i-1]:
                    yield ' '
            yield char


    def generate(self, *resource_names, view=None, stacked=None, region=None, period=None, title=None, **kw):
        if view is None:
            view = self.view
        if stacked is None:
            stacked = self.stacked
        if region is None:
            region = self.region
        if period is None:
            period = self.period
        if title is None:
            title = self.title
        return {
            'metrics': self.metrics.generate(*resource_names, **kw),
            'view': view,
            'stacked': stacked,
            'region': region,
            'period': period,
            'title': title
        }


class Metrics:
    def __init__(self, namespace, resource_type, conf):
        self.namespace = namespace
        self.resource_type = resource_type
        self.metrics = [Metric(namespace, resource_type, metric) for metric in conf['metrics']]

    def generate(self, *resource_names, **kw):
        metrics = [
            metric.generate(*resource_names, **kw) for metric in self.metrics
        ]
        for i, metric in enumerate(metrics[1:]):
            curr_i = i + 1
            while metrics[i][0] == '...' or len(metrics[i]) == 1 or metrics[i][0] == '.':
                i -= 1
                if i < 0:
                    break
            if i < 0:
                continue
            if metric[:-1] == metrics[i][:-1]:
                metrics[curr_i] = ['...', metric[-1]]
                continue
            for j, val in enumerate(metric[:-1]):
                if val == metrics[i][j]:
                    metrics[curr_i][j] = '.'
        return metrics


class Metric:
    def __init__(self, namespace, resource_type, conf):
        if type(conf) is str:
            self.namespace = namespace
            self.resource_type = resource_type
            self.metric_name = conf
            self.config = {'stat': 'Sum'}
            return
        if len(conf) <= 2:
            self.namespace = namespace
            self.resource_type = resource_type
            if len(conf) == 1:
                if type(conf[0]) is str:
                    self.metric_name = conf
                    self.config = {}
                else:
                    self.metric_name = None
                    self.config = conf[0]
            else:
                self.metric_name, self.config = conf
        else:
            if len(conf) == 4:
                self.namespace, self.metric_name, self.resource_type, self.config = conf
            else:
                raise ValueError(f"Couldn't parse conf: {conf}")
        if 'stat' not in self.config:
            self.config['stat'] = 'Sum'

    def generate(self, *resource_names, **kw):
        if self.metric_name is None:
            return [dict(self.config, **kw)]
        resource_types = [self.resource_type] if type(self.resource_type) is str else self.resource_type
        if self.metric_name == '...':
            return ['...', dict(self.config, **kw)]
        return [self.namespace, self.metric_name, *[elem for pair in zip(resource_types, resource_names) for elem in pair], dict(self.config, **kw)]


for (namespace, resource_type), conf in config.items():
    section = section_by_namespace.get(namespace, 'NoSection')
    for property_conf in conf:
        Widget(section, namespace, resource_type, property_conf)
