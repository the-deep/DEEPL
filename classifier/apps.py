from django.apps import AppConfig


class ClassifierConfig(AppConfig):
    name = 'classifier'

    def ready(self):
        from classifier.globals import init
        init()
