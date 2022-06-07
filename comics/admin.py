from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Genre)
admin.site.register(Comic)
admin.site.register(Chapter)
admin.site.register(ChapterImage)
admin.site.register(ReadHistory)
admin.site.register(BuyList)
admin.site.register(Library)
admin.site.register(Rating)
admin.site.register(Like)
