from artifact_recommender.models import Dataset, Tag, BuildingBlock
from artifact_recommender import serializers
from django.http import Http404
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


class DatasetList(APIView):
    def get(self, request, format=None):
        datasets = Dataset.objects.all()
        serializer = serializers.DatasetSerializer(datasets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        with transaction.atomic():
            for tag_name in request.data['tags']:
                try:
                    tag = Tag.objects.get(name=tag_name)
                except Tag.DoesNotExist:
                    tag = Tag(name=tag_name)
                    tag.save()
            serializer = serializers.DatasetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


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
        for tag_name in request.data['tags']:
            try:
                Tag.objects.get(name=tag_name)
            except Tag.DoesNotExist:
                tag = Tag(name=tag_name)
                tag.save()
        serializer = serializers.DatasetSerializer(dataset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dataset = self.get_object(pk)
        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BuildingBlockList(APIView):
    def get(self, request, format=None):
        building_blocks = BuildingBlock.objects.all()
        serializer = serializers.BuildingBlockSerializer(building_blocks,
                                                         many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        with transaction.atomic():
            for tag_name in request.data['tags']:
                try:
                    tag = Tag.objects.get(name=tag_name)
                except Tag.DoesNotExist:
                    tag = Tag(name=tag_name)
                    tag.save()
            serializer = serializers.BuildingBlockSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class BuildingBlocktDetail(APIView):
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
        for tag_name in request.data['tags']:
            try:
                Tag.objects.get(name=tag_name)
            except Tag.DoesNotExist:
                tag = Tag(name=tag_name)
                tag.save()
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
