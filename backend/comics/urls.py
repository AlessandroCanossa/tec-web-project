from django.urls import path, include

from . import views

app_name = 'comics'
urlpatterns = [
    path('', views.index, name='index'),
    path('comics/', include([
        path('', views.comics_list, name='comic_list'),
        path('<int:comic_id>/', views.comic_details, name='comic_detail'),
        path('<int:comic_id>/chapter-<int:chapter_id>/', views.chapter_details, name='chapter_detail'),
        path('like_chapter/<int:chapter_id>/', views.like_chapter, name='like_chapter'),
        path('buy_chapter/<int:chapter_id>/', views.buy_chapter, name='buy_chapter'),
        path('rate_comic/<int:comic_id>/<int:rating>', views.add_rating, name='rate_comic'),
        path('save_bookmark/<int:comic_id>', views.add_bookmark, name='add_bookmark'),
    ])),

    path('comments/', include([
        path('add/<int:chapter_id>', views.add_comment, name='add_comment'),
        path('delete/<int:comment_id>', views.delete_comment, name='delete_comment'),
    ])),

    path('account/', include('django.contrib.auth.urls')),
    path('signup/', views.register, name='signup'),

    path('user/', include([
        path('<int:user_id>/', views.user_details, name='user_detail'),
        path('profile/', views.profile, name='profile'),
        path('settings/', views.settings, name='settings'),
        # path('signout/', views.logout, name='logout'),
    ])),
]
