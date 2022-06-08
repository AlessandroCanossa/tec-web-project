from django.contrib import admin

# Register your models here.
from comments.models import Comment, CommentLike, CommentDislike

admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(CommentDislike)
