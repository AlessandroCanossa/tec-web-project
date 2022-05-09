from django.contrib import admin
from .models import User, Comic, Genre

# Register your models here.

admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Comic)
