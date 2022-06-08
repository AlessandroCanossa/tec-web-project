from django.contrib import admin

# Register your models here.
from comments.models import Comment


class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'chapter', 'body', 'created_on', 'reply')
    list_filter = ('created_on', 'chapter', 'user')
    search_fields = ('user__username__contains',)
    exclude = ('created_on',)


admin.site.register(Comment, CommentModelAdmin)
