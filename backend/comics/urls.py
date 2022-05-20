from django.urls import path

from . import views

app_name = 'comics'
urlpatterns = [
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/new', views.UserCreate.as_view(), name='user-create'),
    path('users/<int:pk>', views.UserDetails.as_view(), name='user-details'),
    path('users/<int:user_id>/library', views.LibraryList.as_view(), name='user-library'),
    path('library/entry/<int:pk>/delete',  views.LibraryDelete.as_view(), name='library-entry-delete'),
    path('library/entry/new',  views.LibraryAdd.as_view(), name='library-entry-add'),
    path('comics/', views.ComicList.as_view(), name='comic-list'),
    path('comics/new', views.ComicCreate.as_view(), name='comic-create'),
    path('comics/<int:pk>', views.ComicDetails.as_view(), name='comic-details'),
    path('comics/<int:comic_id>/chapters', views.ChapterList.as_view(), name='chapter-list'),
    path('chapter/new', views.ChapterCreate.as_view(), name='chapter-create'),
    path('chapter/<int:pk>', views.ChapterDetails.as_view(), name='chapter-details'),
    path('chapter/<int:chapter>/images', views.ChapterImageList.as_view(), name='chapter-image-list'),
    path('genres', views.GenreList.as_view(), name='genre-list')
]
