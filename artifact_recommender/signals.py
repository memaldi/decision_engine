from django.db.models.signals import post_save
from django.dispatch import receiver
from artifact_recommender.models import Dataset


@receiver(post_save, sender=Dataset)
def similarity_callback(sender, instance, **kwargs):
    print(sender)
    print(instance)
    print(kwargs)
