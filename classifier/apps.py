from django.apps import AppConfig


class ClassifierConfig(AppConfig):
    name = 'classifier'

    def ready(self):
        import classifier.receivers  # noqa
        from classifier.globals import init
        init()
