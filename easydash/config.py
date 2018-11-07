'''EasyDash command line utilities'''
CONFIG = {
    'ecs-service': {
        'click': (
            ('service', '--service', '-s', {'required': True}),
            ('cluster', '--cluster', '-c', {'required': True}),
            ('service-name', '-st', {
                'required': False
            })
        )
    }
}
