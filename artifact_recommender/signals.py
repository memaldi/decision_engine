from django.db.models.signals import post_save
from django.dispatch import receiver
from artifact_recommender.models import Dataset
from redis import Redis
from rq import Queue

q = Queue(connection=Redis())


@receiver(post_save, sender=Dataset)
def similarity_callback(sender, instance, **kwargs):
    #TODO: call similarity function
    pass
