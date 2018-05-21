from django.apps import AppConfig


class CfpConfig(AppConfig):
    name = 'cfp'

    def ready(self):
        from . import signals  # noqa
