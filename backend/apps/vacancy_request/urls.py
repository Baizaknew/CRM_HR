from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.vacancy_request.views import VacancyRequestModelViewSet, \
    VacancyRequestCommentViewSet

router = DefaultRouter()
router.register(r'', VacancyRequestModelViewSet, basename='vacancy-request')
router.register('comments', VacancyRequestCommentViewSet, basename='vacancy-request-comments')

urlpatterns = [
    path('', include(router.urls)),
]
