from rest_framework import serializers
from artifact_recommender.models import Dataset, Tag, BuildingBlock


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


class BuildingBlockSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, slug_field='name',
                                        queryset=Tag.objects.all())

    class Meta:
        model = BuildingBlock
        fields = ('id', 'lang', 'tags')
