from django.urls import path, include
from rest_framework import routers
from comics import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/auth/', include('rest_framework.urls', namespace='rest_framework'))
]
