from rest_framework.routers import DefaultRouter

from django.urls import path, include

from apps.vacancy.views import VacancyModelViewSet, VacancyCommentViewSet

router = DefaultRouter()
router.register('comments', VacancyCommentViewSet, basename='vacancy-comments')
router.register('', VacancyModelViewSet, basename='vacancy')

urlpatterns = [
    path('', include(router.urls)),
]
