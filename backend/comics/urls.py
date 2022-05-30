from django.urls import path, include

from . import views

app_name = 'comics'
urlpatterns = [
    path('', views.index, name='index'),
    # path('login/', views.login, name='login'),
    # path('registration/', views.registration, name='registration'),
    path('comics/', include([
        path('', views.comics_list, name='comic_list'),
        path('<int:comic_id>/', views.comic_details, name='comic_detail'),
        path('rate_comic/<int:comic_id>/<int:rating>', views.add_rating, name='rate_comic'),
        path('save_bookmark/<int:comic_id>', views.add_bookmark, name='add_bookmark'),
    ]))
]
