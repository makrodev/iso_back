from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings, views
from .settings import MEDIA_ROOT

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/app/', include('api.urls_app')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=MEDIA_ROOT)

