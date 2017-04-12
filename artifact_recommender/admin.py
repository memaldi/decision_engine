from django.contrib import admin
from artifact_recommender.models import Dataset, BuildingBlock, Application
from artifact_recommender.models import Tag
# Register your models here.

admin.site.register(Dataset)
admin.site.register(BuildingBlock)
admin.site.register(Application)
admin.site.register(Tag)
