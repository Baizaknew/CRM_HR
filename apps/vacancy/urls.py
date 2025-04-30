from rest_framework.routers import DefaultRouter

from django.urls import path, include

from apps.vacancy.views import VacancyModelViewSet

router = DefaultRouter()
router.register('', VacancyModelViewSet, basename='vacancy')

urlpatterns = [
    path('', include(router.urls)),
]
