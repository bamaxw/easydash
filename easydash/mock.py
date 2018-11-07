'''Mock easydash objects used for debugging and testing'''
import json

class Dashboard:
    def __init__(self, **options):
        self.opts = options

    def get(self, *bundles):
        return

    def to_json(self, **opts):
        return json.dumps(self.opts, **opts)


class ServiceDashboard(Dashboard):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
