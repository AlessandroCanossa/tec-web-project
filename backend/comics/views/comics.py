from django.http import Http404
from rest_framework import views, status, authentication, permissions, generics
from rest_framework.response import Response
from rest_framework.request import Request
import django_filters.rest_framework

from ..models import Comic, Chapter, ChapterImage, Genre
from ..serializers import *


class ComicList(generics.ListAPIView):
    serializer_class = ComicListSerializer
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


class ChapterList(views.APIView):
    def get(self, request: Request, comic_id: int, format=None) -> Response:
        chapters = Chapter.objects.filter(comic_id=comic_id)

        serializer = ChapterListSerializer(chapters, many=True, context={'request': request})

        return Response(data=serializer.data)


class ChapterCreate(generics.CreateAPIView):
    serializer_class = ChapterSerializer


class ChapterDetails(views.APIView):

    @staticmethod
    def get_object(pk: int):
        try:
            return Chapter.objects.get(pk=pk)
        except Chapter.DoesNotExist:
            raise Http404

    def get(self, request: Request, pk: int, format=None) -> Response:
        chapter = self.get_object(pk)

        serializer = ChapterSerializer(chapter, context={'request': request})

        return Response(data=serializer.data)

    def delete(self, request: Request, pk: int, format=None) -> Response:
        chapter = self.get_object(pk)

        if chapter.comic.creator.pk != request.user.pk:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        chapter.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request: Request, pk: int, format=None) -> Response:
        chapter = self.get_object(pk)

        if chapter.comic.creator.pk != request.user.pk:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ChapterSerializer(chapter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChapterImageList(views.APIView):
    @staticmethod
    def get_chapter(pk):
        try:
            return Chapter.objects.get(pk)
        except Chapter.DoesNotExist:
            raise Http404

    def get(self, request: Request, chapter: int, format=None) -> Response:
        chapter = self.get_chapter(chapter)
        images = ChapterImage.objects.filter(chapter_id=chapter)

        serializer = ChapterImageSerializer(images, many=True, context={'request': request})

        return Response(data=serializer.data)

    def post(self, request: Request, chapter: int, format=None) -> Response:
        chapter = self.get_chapter(chapter)

        if chapter.comic.creator.pk != request.user.pk:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ChapterImageSerializer(data=request.data, many=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreList(generics.ListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
