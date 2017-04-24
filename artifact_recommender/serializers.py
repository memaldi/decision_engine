from rest_framework import serializers
from artifact_recommender.models import Dataset, Tag, BuildingBlock
from artifact_recommender.models import Application, Idea


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


class ApplicationSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, slug_field='name',
                                        queryset=Tag.objects.all())

    class Meta:
        model = Application
        fields = ('id', 'lang', 'tags', 'scope', 'min_age')


class IdeaSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, slug_field='name',
                                        queryset=Tag.objects.all())

    class Meta:
        model = Idea
        fields = ('id', 'lang', 'tags')
