from rest_framework.routers import DefaultRouter

from django.urls import path, include

from apps.vacancy.views import VacancyModelViewSet, VacancyCommentViewSet, VacancyStatusViewSet

router = DefaultRouter()
router.register('statuses', VacancyStatusViewSet, basename='vacancy-statuses')
router.register('comments', VacancyCommentViewSet, basename='vacancy-comments')
router.register('', VacancyModelViewSet, basename='vacancy')

urlpatterns = [
    path('', include(router.urls)),
]
