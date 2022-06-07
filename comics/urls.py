from django.urls import path, include

from . import views

app_name = 'comics'
urlpatterns = [
    path('', views.index, name='index'),
    path('comics/', include([
        path('', views.comics_list, name='comic_list'),

        path('<int:comic_id>/', views.comic_details, name='comic_detail'),
        path('<int:comic_id>/chapter-<int:chapter_id>/', views.chapter_details, name='chapter_detail'),
        path('<int:comic_id>/delete/', views.delete_comic, name='delete_comic'),
        path('<int:comic_id>/status/<str:status_id>/', views.change_comic_status, name='change_comic_status'),
        path('add_new_comic/', views.new_comic, name='add_new_comic'),

        path('<int:comic_id>/new_chapter', views.new_chapter, name='add_new_chapter'),
        path('delete_chapter/<int:chapter_id>/', views.delete_chapter, name='delete_chapter'),

        path('like_chapter/<int:chapter_id>', views.like_chapter, name='like_chapter'),
        path('buy_chapter/<int:chapter_id>', views.buy_chapter, name='buy_chapter'),
        path('rate_comic/<int:comic_id>/<int:rating>', views.rate_comic, name='rate_comic'),
        path('toggle_bookmark/<int:comic_id>', views.bookmark_comic, name='toggle_bookmark'),

    ])),

    path('comments/', include([

    ])),

    path('account/', include('django.contrib.auth.urls')),
    path('signup/', views.register, name='signup'),

    path('user/', include([
        path('settings/', views.settings, name='settings'),
        path('buy_coins/', views.market, name='buy_coins'),
        path('delete_history_entry/<int:entry_id>', views.delete_history_entry, name='delete_history_entry'),
        path('change_username/', views.change_username, name='change_username'),
        path('change_password/', views.change_password, name='change_password'),
        path('become_creator/', views.become_creator, name='become_creator'),
    ])),
]
