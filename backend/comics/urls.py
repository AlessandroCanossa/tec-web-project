from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'comics'
urlpatterns = format_suffix_patterns([
    path(r'users/', views.UserList.as_view(), name='user-list'),
    path(r'users/<int:pk>/', views.UserDetails.as_view(), name='user-details'),
])
