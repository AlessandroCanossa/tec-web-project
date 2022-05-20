from django.urls import path

from . import views

app_name = 'comics'
urlpatterns = [
    path(r'users/', views.UserList.as_view(), name='user-list'),
    path(r'users/new', views.UserCreate.as_view(), name='user-create'),
    path(r'users/<int:pk>', views.UserDetails.as_view(), name='user-details'),
    path('comics/', views.ComicList.as_view(), name='comic-list'),
    path(r'comics/new', views.ComicCreate.as_view(), name='comic-create'),
    path('comics/<int:pk>', views.ComicDetails.as_view(), name='comic-details'),
    path(r'comics/<int:comic_id>/chapters', views.ChapterList.as_view(), name='chapter-list'),
    path(r'chapter/new', views.ChapterCreate.as_view(), name='chapter-create'),
    path(r'chapter/<int:pk>', views.ChapterDetails.as_view(), name='chapter-details'),
    path(r'chapter/<int:chapter>/images', views.ChapterImageList.as_view(), name='chapter-image-list'),
]
