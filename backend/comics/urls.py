from django.urls import path

from . import views

app_name = 'comics'
urlpatterns = [
    path('', views.index, name='index'),
    # path('login/', views.login, name='login'),
    # path('registration/', views.registration, name='registration'),
    path('series/', views.series_list, name='series'),
    path('series/<int:comic_id>/', views.comic_details, name='comic_detail'),
]
