from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

# URLS del proyecto
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('medidas.urls')),
    re_path('accounts/', include('users.urls')),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
