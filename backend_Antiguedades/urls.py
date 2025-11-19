# backend_Antiguedades/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    # Enlazar la aplicación principal
    path('', include('app_Antiguedades.urls')), 
]

# Configuración para servir archivos media durante el desarrollo (solo si DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)