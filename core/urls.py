from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView

swagger_urls = [
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.user.urls')),
] + swagger_urls
