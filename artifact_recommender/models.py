from django.db import models

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False,
                            db_index=True)

    def __str__(self):
        return self.name


class Artifact(models.Model):
    id = models.IntegerField(primary_key=True)
    lang = models.CharField(max_length=20, null=False, blank=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return '{}\n{}\n{}\n'.format(self.id, self.lang, self.tags.all())


class Dataset(Artifact):
    pass


class BuildingBlock(Artifact):
    pass


class Application(Artifact):
    scope = models.CharField(max_length=20)
    min_age = models.IntegerField(null=True, default=0)


class Idea(Artifact):
    pass


class Similarity(models.Model):
    source_artifact = models.ForeignKey('Artifact',
                                        related_name='source_artifact',
                                        on_delete=models.CASCADE)
    target_artifact = models.ForeignKey('Artifact',
                                        related_name='target_artifact',
                                        on_delete=models.CASCADE)
    value = models.FloatField(null=False)

    class Meta:
        unique_together = (("source_artifact", "target_artifact"),)

    def __str__(self):
        return '{} - {}: {}'.format(self.source_artifact.id,
                                    self.target_artifact.id, self.value)
