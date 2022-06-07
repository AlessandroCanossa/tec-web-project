from django.urls import path, include

from users import views

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.register, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('buy_coins/', views.market, name='buy_coins'),
    path('change_username/', views.change_username, name='change_username'),
    path('change_password/', views.change_password, name='change_password'),
    path('become_creator/', views.become_creator, name='become_creator'),

]
