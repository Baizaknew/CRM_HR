from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView, SpectacularAPIView


api_urls = [
    path('users/', include('apps.user.urls')),
    path('vacancies/', include('apps.vacancy.urls')),
    path('vacancy-requests/', include('apps.vacancy_request.urls')),
    path('candidates/', include('apps.candidate.urls')),

    # swagger docs
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(), name='redoc'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
]
