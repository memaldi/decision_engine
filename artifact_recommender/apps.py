from django.apps import AppConfig


class ArtifactRecommenderConfig(AppConfig):
    name = 'artifact_recommender'

    def ready(self):
        import artifact_recommender.signals
