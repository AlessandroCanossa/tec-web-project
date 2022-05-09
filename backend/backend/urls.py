from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/v1/auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path('api/v1/', include('comics.urls', namespace='comics'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
