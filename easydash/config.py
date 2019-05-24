GREEN = '#47cc7a'
RED = '#f4415f'
BLUE = '#4286f4'
VIOLET = '#9467bd'

config = {
    ('AWS/ApplicationELB', 'LoadBalancer'): [
        'ConsumedLCUs',
        {'name': 'RequestCount', 'title': 'Total Request Count'},
        {'name': 'TargetResponseTime', 'title': 'Response Time'},
        {
            'name': 'TargetFailedCodes',
            'stacked': True,
            'metrics': [
                ('HTTPCode_Target_4XX_Count', {'color': '#9467bd', 'label': '4xx'}),
                ('HTTPCode_Target_3XX_Count', {'color': '#e377c2', 'label': '3xx'}),
                ('HTTPCode_Target_5XX_Count', {'color': '#d62728', 'label': '5xx'})
            ]
        },
        {
            'name': 'TargetSuccessCodes',
            'stacked': True,
            'metrics': [
                ('HTTPCode_Target_2XX_Count', {'color': '#2ca02c', 'label': '2xx'}),
            ]
        },
        {
            'name': 'TargetResponseCodes',
            'metrics': [
                ('HTTPCode_Target_4XX_Count', {'color': '#9467bd', 'label': '4xx'}),
                ('HTTPCode_Target_2XX_Count', {'color': '#2ca02c', 'label': '2xx'}),
                ('HTTPCode_Target_3XX_Count', {'color': '#e377c2', 'label': '3xx'}),
                ('HTTPCode_Target_5XX_Count', {'color': '#d62728', 'label': '5xx'})
            ]
        },
        {
            'name': 'Connections',
            'metrics': [
                'NewConnectionCount',
                'ActiveConnectionCount'
            ]
        },
        'TargetResponseCount',
        {
            'name': 'ResponseCodes',
            'title': 'Load Balancer Responses',
            'metrics': [
                ('HTTPCode_ELB_4XX_Count', {'color': '#9467bd', 'label': '4xx'}),
                ('HTTPCode_ELB_5XX_Count', {'color': '#d62728', 'label': '5xx'})
            ]
        },
        {
            'name': 'Stats',
            'height': 12,
            'metrics': [
                ["HTTPCode_ELB_5XX_Count", {"id": "elb5", "visible": False, "stat": "Sum"}],
                ["HTTPCode_ELB_4XX_Count", {"id": "elb4", "visible": False, "stat": "Sum"}],
                ["HTTPCode_Target_3XX_Count", {"id": "target3", "visible": False, "stat": "Sum"}],
                ["HTTPCode_Target_5XX_Count", {"id": "target5", "visible": False, "stat": "Sum"}],
                ["HTTPCode_Target_2XX_Count", {"id": "target2", "visible": False, "stat": "Sum"}],
                ["HTTPCode_Target_4XX_Count", {"id": "target4", "visible": False, "stat": "Sum"}],
                [{'expression': 'elb4 + elb5', 'id': 'elb', 'visible': False}],
                [{'expression': 'target2 + target3 + target4 + target5', 'id': 'target', 'visible': False}],
                [{'expression': 'target + elb', 'id': 'all', 'visible': False}],
                [{'expression': 'target * 100 / SUM([target + elb5])', 'label': 'Availability %', 'color': BLUE}],
                [{'expression': 'target2 * 100 / SUM([target2, target5])', 'label': 'OK %', 'color': GREEN}],
            ]
        },
        {
            'name': 'TargetStats',
            'title': 'Target Stats',
            'stacked': True,
            'height': 12,
            'metrics': [
                ["HTTPCode_Target_3XX_Count", {"id": "target3", "visible": False, "stat": "Sum"}],
                ["HTTPCode_Target_5XX_Count", {"id": "target5", "visible": False, "stat": "Sum"}],
                ["HTTPCode_Target_2XX_Count", {"id": "target2", "visible": False, "stat": "Sum"}],
                ["HTTPCode_Target_4XX_Count", {"id": "target4", "visible": False, "stat": "Sum"}],
                [{'expression': 'target2 + target3 + target4 + target5', 'id': 'target', 'visible': False}],
                [{'expression': 'target3 * 100 / target', 'label': '3xx', 'color': '#fca80c'}],
                [{'expression': 'target4 * 100 / target', 'label': '4xx', 'color': VIOLET}],
                [{'expression': 'target5 * 100 / target', 'label': '5xx', 'color': RED}],
                [{'expression': 'target2 * 100 / target', 'label': '2xx', 'color': GREEN}],
            ]
        }
    ],
    ('AWS/ApplicationELB', ('TargetGroup', 'LoadBalancer')): [
        {
            'name': 'HealthyHostCount',
            'metrics': [
                ['HealthyHostCount', {'color': '#2ca02c', 'stat': 'Average'}],
                ['UnHealthyHostCount', {'color': '#f42440', 'stat': 'Average'}]
            ]
        }
    ],
    ('AWS/ApplicationELB', 'TargetGroup'): [
        'RequestCountPerTarget',
        {
            'name': 'RequestCountPerTargetPerSecond',
            'title': 'Request Count Per Target Per Second',
            'metrics': [
                ['RequestCountPerTarget', {'id': 'reqs', 'visible': False, 'stat': 'Sum'}],
                [{'expression': 'reqs / PERIOD(reqs)', 'label': 'rps'}]
            ]
        }
    ],
    ('AWS/ECS', ('ServiceName', 'ClusterName')): [
        {
            'name': 'Memory',
            'metrics': [
                ['MemoryUtilization', {"stat": "Minimum", "color": "#2ca02c"}],
                ["...", {'stat': 'Average', "color": "#1f77b4"}],
                ['...', {"stat": "Maximum", "color": "#d62728"}],
            ],
            'yAxis': {
                'left': {
                    'min': 0,
                    'max': 100
                }
            }
        },
        {
            'name': 'CPU',
            'metrics': [
                ['CPUUtilization', {"stat": "Minimum", "color": "#2ca02c"}],
                ["...", {'stat': 'Average', "color": "#1f77b4"}],
                ['...', {"stat": "Maximum", "color": "#d62728"}],
            ],
            'yAxis': {
                'left': {
                    'min': 0,
                    'max': 100
                }
            }
        }
    ]
}

section_by_namespace = {
    'AWS/ApplicationELB': 'ALB',
    'AWS/ECS': 'ECS'
}
