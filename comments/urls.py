from django.urls import path, include

from . import views

app_name = 'comments'

urlpatterns = [
    path('add/<int:chapter_id>', views.add_comment, name='add_comment'),
    path('delete/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('like/<int:comment_id>', views.like_comment, name='like_comment'),
    path('dislike/<int:comment_id>', views.dislike_comment, name='dislike_comment'),
]
