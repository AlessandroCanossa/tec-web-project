from django.contrib import admin
from .models import *


# Register your models here.

class ComicModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'status')
    list_filter = ('creator', 'status')
    search_fields = ('title__contains', 'creator__username__contains',)
    exclude = ()


class ChapterModelAdmin(admin.ModelAdmin):
    list_display = ('chapter_num', 'comic', 'pub_date', 'likes', 'cost')
    list_filter = ('comic', 'pub_date')
    search_fields = ('comic__title__contains', 'chapter_num__contains',)
    exclude = ()


class ChapterImageModelAdmin(admin.ModelAdmin):
    list_display = ('image', 'chapter')
    list_filter = ('chapter',)
    search_fields = ('image__name__contains',)
    exclude = ()


class RatingModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'comic', 'rating')
    list_filter = ('user', 'comic', 'rating')
    search_fields = ('user__username__contains', 'comic__title__contains')
    exclude = ()


class LikeModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'chapter')
    list_filter = ('user', 'chapter')
    search_fields = ('user__username__contains', 'chapter__comic__title__contains')
    exclude = ()


class BuyListModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'chapter', 'date')
    list_filter = ('user', 'chapter', 'date')
    search_fields = ('user__username__contains', 'chapter__comic__title__contains')
    exclude = ()


class ReadHistoryModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'chapter', 'date')
    list_filter = ('user', 'chapter', 'date')
    search_fields = ('user__username__contains', 'chapter__comic__title__contains')
    exclude = ()


class LibraryModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'comic')
    list_filter = ('user', 'comic')
    search_fields = ('user__username__contains', 'comic__title__contains')
    exclude = ()


admin.site.register(Genre)
admin.site.register(Comic, ComicModelAdmin)
admin.site.register(Chapter, ChapterModelAdmin)
admin.site.register(ChapterImage, ChapterImageModelAdmin)
admin.site.register(ReadHistory, ReadHistoryModelAdmin)
admin.site.register(BuyList, BuyListModelAdmin)
admin.site.register(Library, LibraryModelAdmin)
admin.site.register(Rating, RatingModelAdmin)
admin.site.register(Like, LikeModelAdmin)
