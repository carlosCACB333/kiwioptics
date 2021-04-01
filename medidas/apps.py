from django.apps import AppConfig


class MedidasConfig(AppConfig):
    name = 'medidas'

    def ready(self):
        import medidas.signals
