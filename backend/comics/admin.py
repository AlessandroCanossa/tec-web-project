from django.contrib import admin
from .models import User, Comic, Genre, Chapter, ChapterImage, ReadHistory, BuyList, Comment

# Register your models here.

admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Comic)
admin.site.register(Chapter)
admin.site.register(ChapterImage)
admin.site.register(ReadHistory)
admin.site.register(BuyList)
admin.site.register(Comment)
