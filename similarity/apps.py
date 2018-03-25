from django.apps import AppConfig


class SimilarityConfig(AppConfig):
    name = 'similarity'

    def ready(self):
        from similarity.globals import init
        init()
