from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from artifact_recommender import models
from artifact_recommender.recommender import tag_similarity
import django_rq


@receiver(m2m_changed, sender=models.Artifact.tags.through)
def similarity_callback(sender, instance, signal, action, reverse, model,
                        pk_set, **kwargs):
    if action == 'post_add':
        django_rq.enqueue(tag_similarity, instance.id)
