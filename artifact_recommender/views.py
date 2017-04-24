from artifact_recommender.models import Dataset, Tag
from artifact_recommender.serializers import DatasetSerializer
from django.http import Http404
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


class DatasetList(APIView):
    def get(self, request, format=None):
        datasets = Dataset.objects.all()
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        with transaction.atomic():
            tags = []
            for tag_name in request.data['tags']:
                try:
                    tag = Tag.objects.get(name=tag_name)
                except Tag.DoesNotExist:
                    tag = Tag(name=tag_name)
                    tag.save()
                tags.append(tag)

            dataset = Dataset(id=request.data['id'], lang=request.data['lang'])
            dataset.save()
            dataset.tags = tags
            dataset.save()
            serializer = DatasetSerializer(dataset)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)


class DatasetDetail(APIView):
    def get_object(self, pk):
        try:
            return Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dataset = self.get_object(pk)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)
