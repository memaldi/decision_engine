from django.db import models

# Create your models here.


class Artifact(models.Model):
    lang = models.CharField(max_length=20)

    class Meta:
        abstract = True


class Dataset(Artifact):
    pass


class BuildingBlock(Artifact):
    pass


class Application(Artifact):
    scope = models.CharField(max_length=20)
    lat = models.FloatField()
    lon = models.FloatField()
    min_age = models.IntegerField()
