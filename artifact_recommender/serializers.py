from rest_framework import serializers
from artifact_recommender.models import Dataset, Tag


class DatasetSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, slug_field='name',
                                        queryset=Tag.objects.all())

    class Meta:
        model = Dataset
        fields = ('id', 'lang', 'tags')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
