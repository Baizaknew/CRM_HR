from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VacancyRequestModelViewSet
from ..user.urls import urlpatterns

router = DefaultRouter()
router.register(r'vacancy-requests', VacancyRequestModelViewSet, basename='vacancy-request')

urlpatterns = [
    path('', include(router.urls)),
]