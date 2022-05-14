from rest_framework import serializers

from ..models import Comic, Chapter, ChapterImage, Genre


class ComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = '__all__'


class ComicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = ['id', 'title', 'thumbnail', 'rating', 'status']


class ComicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = ['title', 'creator', 'thumbnail', 'cover', 'genre', 'summary']


class ChapterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'title', 'cost', 'pub_date']


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'


class ChapterImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterImage
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
