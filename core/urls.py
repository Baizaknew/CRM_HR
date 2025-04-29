from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView, SpectacularAPIView

swagger_urls = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(), name='redoc'),
]

api_urls = [
    path('users/', include('apps.user.urls')),
    path('vacancies/', include('apps.vacancy_request.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
] + swagger_urls
