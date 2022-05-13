from django.http import Http404
from rest_framework import views, status, authentication, permissions, generics
from rest_framework.response import Response
from rest_framework.request import Request
import django_filters.rest_framework

from ..models import Comic
from ..serializers import ComicSerializer, ComicListSerializer, ComicCreateSerializer


class ComicList(generics.ListAPIView):
    serializer_class = ComicListSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    queryset = Comic.objects.all()
    filterset_fields = ['genre', 'status']


class ComicCreate(generics.CreateAPIView):
    serializer_class = ComicCreateSerializer


class ComicDetails(views.APIView):
    @staticmethod
    def get_object(pk: int) -> Comic:
        try:
            return Comic.objects.get(pk=pk)
        except Comic.DoesNotExist:
            raise Http404

    def get(self, request: Request, pk: int, format=None) -> Response:
        comic = self.get_object(pk)

        serializer = ComicSerializer(comic, context={'request': request})

        return Response(data=serializer.data)

    def delete(self, request: Request, pk: int, format=None) -> Response:
        comic = self.get_object(pk)
        if comic.creator.pk != request.user.pk:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        comic.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request: Request, pk: int, format=None) -> Response:
        comic = self.get_object(pk)

        if comic.creator.pk != request.user.pk:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ComicSerializer(comic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
