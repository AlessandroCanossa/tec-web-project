from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Comic)
admin.site.register(Chapter)
admin.site.register(ChapterImage)
admin.site.register(ReadHistory)
admin.site.register(BuyList)
admin.site.register(Comment)
admin.site.register(CoinsPurchase)
admin.site.register(Library)
admin.site.register(Rating)
admin.site.register(Like)
