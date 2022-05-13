from django.urls import path

from . import views

app_name = 'comics'
urlpatterns = [
    path(r'users/', views.UserList.as_view(), name='user-list'),
    path(r'users/new', views.UserCreate.as_view(), name='user-create'),
    path(r'users/<int:pk>', views.UserDetails.as_view(), name='user-details'),
    path(r'comics/series', views.ComicList.as_view(), name='comic-list'),
    path(r'comics/new', views.ComicCreate.as_view(), name='comic-create'),
    path(r'comics/<int:pk>', views.ComicDetails.as_view(), name='comic-details'),
]
