config = {
    ('AWS/ApplicationELB', 'LoadBalancer'): [
        'ConsumedLCUs',
        {'name': 'RequestCount', 'title': 'Total Request Count'},
        {'name': 'TargetResponseTime', 'title': 'ResponseTime'},
        {
            'name': 'TargetResponseCodes',
            'metrics': [
                ('HTTPCode_Target_4XX_Count', {'color': '#9467bd', 'label': '4xx'}),
                ('HTTPCode_Target_2XX_Count', {'color': '#2ca02c', 'label': '2xx'}),
                ('HTTPCode_Target_3XX_Count', {'color': '#e377c2', 'label': '3xx'}),
                ('HTTPCode_Target_5XX_Count', {'label': '5xx'})
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
            'metrics': [
                ('HTTPCode_ELB_4XX_Count', {'color': '#9467bd', 'label': '4xx'}),
                ('HTTPCode_ELB_5XX_Count', {'color': '#d62728', 'label': '5xx'})
            ]
        },
        {
            'name': 'Stats',
            'metrics': [
                [ { "expression": "SUM([m3,m4,m5,m6])*100/SUM(METRICS())", "label": "Availability %", "id": "e1", "stat": "Sum", "color": "#1f77b4" } ],
                [ { "expression": "m5*100/SUM([m3,m4,m5,m6])", "label": "Response OK %", "id": "e2", "color": "#2ca02c" } ],
                ["HTTPCode_ELB_5XX_Count", { "id": "m1", "visible": False, "stat": "Sum" } ],
                ["HTTPCode_ELB_4XX_Count", { "id": "m2", "visible": False, "stat": "Sum" } ],
                ["HTTPCode_Target_3XX_Count", { "id": "m3", "visible": False, "stat": "Sum" } ],
                ["HTTPCode_Target_5XX_Count", { "id": "m4", "visible": False, "stat": "Sum" } ],
                ["HTTPCode_Target_2XX_Count", { "id": "m5", "visible": False, "stat": "Sum" } ],
                ["HTTPCode_Target_4XX_Count", { "id": "m6", "visible": False, "stat": "Sum" } ]
            ]
        }
    ],
    ('AWS/ApplicationELB', 'TargetGroup'): [
        'RequestCountPerTarget'
    ],
    ('AWS/ECS', ('ServiceName', 'ClusterName')): [
        {
            'name': 'Memory',
            'metrics': [
                [ 'MemoryUtilization', { "stat": "Minimum", "color": "#2ca02c" } ],
                [ "...", { 'stat': 'Average', "color": "#1f77b4" } ],
                [ '...', { "stat": "Maximum", "color": "#d62728" } ],
            ]
        },
        {
            'name': 'CPU',
            'metrics': [
                [ 'CPUUtilization', { "stat": "Minimum", "color": "#2ca02c" } ],
                [ "...", { 'stat': 'Average', "color": "#1f77b4" } ],
                [ '...', { "stat": "Maximum", "color": "#d62728" } ],
            ]
        }
    ]
}

section_by_namespace = {
    'AWS/ApplicationELB': 'ALB',
    'AWS/ECS': 'ECS'
}
