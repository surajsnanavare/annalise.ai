from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.swagger import schema_view

urlpatterns = [
     # API documentation - Swagger
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-redoc'),

    # Django admin
    path("admin/", admin.site.urls),

    path(settings.API_PREFIX + 'users/', include('users.api.urls')),
    path(settings.API_PREFIX + 'auth/', include('authentication.api.urls')),
    path(settings.API_PREFIX + 'image/', include('images.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
