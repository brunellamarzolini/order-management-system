from django.apps import AppConfig

class OmsConfig(AppConfig):
    name = 'oms'

    def ready(self):
        import oms.cache_signals