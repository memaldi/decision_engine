from enum import Enum

from artifact_recommender import recommender, serializers
from artifact_recommender.models import (Application, Artifact, BuildingBlock,
                                         Dataset, Idea, Similarity, Tag)
from django.core.cache import cache
from django.db import transaction
from django.db.models import Q
from django.http import Http404, HttpResponseBadRequest
from rest_framework import serializers as rest_serializers
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from silk.profiling.profiler import silk_profile

# Create your views here.


class ArtifactType(Enum):
    DATASET = "dataset"
    BUILDING_BLOCK = "buildingblock"
    APP = "app"
    IDEA = "idea"
    ARTIFACT = "artifact"


@permission_classes((IsAuthenticatedOrReadOnly,))
class DatasetList(APIView):
    def get(self, request, format=None):
        datasets = Dataset.objects.all()
        serializer = serializers.DatasetSerializer(datasets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        with transaction.atomic():
            with silk_profile("Stem tags"):
                stemmed_tags = recommender.stem_tags(request.data['lang'],
                                                     request.data['tags'])
            request.data['tags'] = stemmed_tags
            for tag_name in request.data['tags']:
                if not cache.get('tag:{}'.format(tag_name)):
                    if not Tag.objects.filter(name=tag_name).exists():
                        tag = Tag(name=tag_name)
                        tag.save()
                        cache.set('tag:{}'.format(tag_name), tag.id)
            serializer = serializers.DatasetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticatedOrReadOnly,))
class DatasetDetail(APIView):
    def get_object(self, pk):
        try:
            return Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dataset = self.get_object(pk)
        serializer = serializers.DatasetSerializer(dataset)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        dataset = self.get_object(pk)
        with silk_profile("Stem tags"):
            stemmed_tags = recommender.stem_tags(request.data['lang'],
                                                 request.data['tags'])
        request.data['tags'] = stemmed_tags
        for tag_name in request.data['tags']:
            if not cache.get('tag:{}'.format(tag_name)):
                if not Tag.objects.filter(name=tag_name).exists():
                    tag = Tag(name=tag_name)
                    tag.save()
                    cache.set('tag:{}'.format(tag_name), tag.id)
        serializer = serializers.DatasetSerializer(dataset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dataset = self.get_object(pk)
        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes((IsAuthenticatedOrReadOnly,))
class ArtifactRecommendation(APIView):
    def get_object(self, pk, _type):
        try:
            artifact = Artifact.objects.get(pk=pk)
            return self.filter_type(artifact, _type)
        except Artifact.DoesNotExist:
            raise Http404

    def filter_type(self, artifact, _type):
        try:
            if ArtifactType(_type) == ArtifactType.DATASET:
                artifact.dataset
            elif ArtifactType(_type) == ArtifactType.BUILDING_BLOCK:
                artifact.buildingblock
            elif ArtifactType(_type) == ArtifactType.APP:
                artifact.application
            elif ArtifactType(_type) == ArtifactType.IDEA:
                artifact.idea
            return artifact
        except Artifact.DoesNotExist:
            raise Http404

    def get(self, request, source, pk, target, format=None):
        try:
            artifact = self.get_object(pk, source)
            with silk_profile("Get similarity"):
                if ArtifactType(target) == ArtifactType.ARTIFACT:
                    similarity = Similarity.objects.filter(
                        Q(source_artifact=artifact) |
                        Q(target_artifact=artifact)) \
                            .order_by('-value')
                else:
                    if target == 'app':
                        target = 'application'
                    similarity = Similarity.objects.filter(
                        Q(source_artifact=artifact,
                          **{'target_artifact__' + target + '__isnull':
                             False}) |
                        Q(target_artifact=artifact,
                          **{'source_artifact__' + target + '__isnull':
                             False})).order_by('-value')
            similar_datasets = []
            with silk_profile("Similarity loop"):
                for sim in similarity:
                    if sim.source_artifact.id == artifact.id:
                        similar_datasets.append(sim.target_artifact.id)
                    else:
                        similar_datasets.append(sim.source_artifact.id)
            return Response(similar_datasets)
        except ValueError as e:
            return HttpResponseBadRequest("Bad request. Is the URL correct?")


@permission_classes((IsAuthenticatedOrReadOnly,))
class BuildingBlockList(APIView):
    def get(self, request, format=None):
        building_blocks = BuildingBlock.objects.all()
        serializer = serializers.BuildingBlockSerializer(building_blocks,
                                                         many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        with transaction.atomic():
            with silk_profile("Stem tags"):
                stemmed_tags = recommender.stem_tags(request.data['lang'],
                                                     request.data['tags'])
            request.data['tags'] = stemmed_tags
            for tag_name in request.data['tags']:
                if not cache.get('tag:{}'.format(tag_name)):
                    if not Tag.objects.filter(name=tag_name).exists():
                        tag = Tag(name=tag_name)
                        tag.save()
                        cache.set('tag:{}'.format(tag_name), tag.id)
            serializer = serializers.BuildingBlockSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticatedOrReadOnly,))
class BuildingBlockDetail(APIView):
    def get_object(self, pk):
        try:
            return BuildingBlock.objects.get(pk=pk)
        except BuildingBlock.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        building_block = self.get_object(pk)
        serializer = serializers.BuildingBlockSerializer(building_block)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        building_block = self.get_object(pk)
        with silk_profile("Stem tags"):
            stemmed_tags = recommender.stem_tags(request.data['lang'],
                                                 request.data['tags'])
        request.data['tags'] = stemmed_tags
        for tag_name in request.data['tags']:
            if not cache.get('tag:{}'.format(tag_name)):
                if not Tag.objects.filter(name=tag_name).exists():
                    tag = Tag(name=tag_name)
                    tag.save()
                    cache.set('tag:{}'.format(tag_name), tag.id)
        serializer = serializers.BuildingBlockSerializer(building_block,
                                                         data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        building_block = self.get_object(pk)
        building_block.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes((IsAuthenticatedOrReadOnly,))
class ApplicationList(APIView):
    def get(self, request, format=None):
        apps = Application.objects.all()
        serializer = serializers.ApplicationSerializer(apps,
                                                       many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        with transaction.atomic():
            with silk_profile(name='Stemming tags'):
                stemmed_tags = recommender.stem_tags(request.data['lang'],
                                                     request.data['tags'])
            request.data['tags'] = stemmed_tags
            with silk_profile(name='Saving tags'):
                for tag_name in request.data['tags']:
                    if not cache.get('tag:{}'.format(tag_name)):
                        if not Tag.objects.filter(name=tag_name).exists():
                            tag = Tag(name=tag_name)
                            tag.save()
                            cache.set('tag:{}'.format(tag_name), tag.id)
            serializer = serializers.ApplicationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticatedOrReadOnly,))
class ApplicationDetail(APIView):
    def get_object(self, pk):
        try:
            return Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        application = self.get_object(pk)
        serializer = serializers.ApplicationSerializer(application)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        application = self.get_object(pk)
        stemmed_tags = recommender.stem_tags(request.data['lang'],
                                             request.data['tags'])
        request.data['tags'] = stemmed_tags
        for tag_name in request.data['tags']:
            if not cache.get('tag:{}'.format(tag_name)):
                if not Tag.objects.filter(name=tag_name).exists():
                    tag = Tag(name=tag_name)
                    tag.save()
                    cache.set('tag:{}'.format(tag_name), tag.id)
        serializer = serializers.ApplicationSerializer(application,
                                                       data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        application = self.get_object(pk)
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes((IsAuthenticatedOrReadOnly,))
class IdeaList(APIView):
    def get(self, request, format=None):
        ideas = Idea.objects.all()
        serializer = serializers.IdeaSerializer(ideas,
                                                many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        with transaction.atomic():
            with silk_profile("Stem tags"):
                stemmed_tags = recommender.stem_tags(request.data['lang'],
                                                     request.data['tags'])
            request.data['tags'] = stemmed_tags
            for tag_name in request.data['tags']:
                if not cache.get('tag:{}'.format(tag_name)):
                    if not Tag.objects.filter(name=tag_name).exists():
                        tag = Tag(name=tag_name)
                        tag.save()
                        cache.set('tag:{}'.format(tag_name), tag.id)
            serializer = serializers.IdeaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticatedOrReadOnly,))
class IdeaDetail(APIView):
    def get_object(self, pk):
        try:
            return Idea.objects.get(pk=pk)
        except Idea.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        idea = self.get_object(pk)
        serializer = serializers.IdeaSerializer(idea)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        idea = self.get_object(pk)
        with silk_profile("Stem tags"):
            stemmed_tags = recommender.stem_tags(request.data['lang'],
                                                 request.data['tags'])
        request.data['tags'] = stemmed_tags
        for tag_name in request.data['tags']:
            if not cache.get('tag:{}'.format(tag_name)):
                if not Tag.objects.filter(name=tag_name).exists():
                    tag = Tag(name=tag_name)
                    tag.save()
                    cache.set('tag:{}'.format(tag_name), tag.id)
        serializer = serializers.IdeaSerializer(idea, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        idea = self.get_object(pk)
        idea.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes((IsAuthenticatedOrReadOnly,))
class UserApps(APIView):
    def get(self, request, user_id, format=None):
        radius = request.GET.get('radius', 10)
        lat = request.GET.get('lat', -1000)
        lon = request.GET.get('lon', -1000)
        errors = []
        try:
            lat = float(lat)
        except ValueError:
            errors.append('lat must be an integer')
        try:
            lon = float(lon)
        except ValueError:
            errors.append('lon must be an integer')
        try:
            radius = float(radius)
        except ValueError:
            errors.append('radius must be an integer')
        if len(errors) > 0:
            raise rest_serializers.ValidationError(errors, code=404)
        app_list = recommender.recommend_app(user_id, lat, lon, radius)
        return Response(app_list)
