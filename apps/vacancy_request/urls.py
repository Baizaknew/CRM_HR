from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.vacancy_request.views import VacancyRequestModelViewSet

router = DefaultRouter()
router.register(r'', VacancyRequestModelViewSet, basename='vacancy-request')

urlpatterns = [
    path('', include(router.urls)),
]
