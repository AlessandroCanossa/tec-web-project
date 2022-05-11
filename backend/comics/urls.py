from django.urls import path

from . import views

app_name = 'comics'
urlpatterns = [
    path(r'users/', views.UserList.as_view(), name='user-list'),
    path(r'users/new', views.UserCreate.as_view(), name='user-create'),
    path(r'users/<int:pk>/', views.UserDetails.as_view(), name='user-details'),
]
