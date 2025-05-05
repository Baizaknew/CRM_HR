from rest_framework.routers import DefaultRouter

from django.urls import path, include

from apps.candidate.views import CandidateModelViewSet

router = DefaultRouter()
router.register('', CandidateModelViewSet, basename='candidate')

urlpatterns = [
    path('', include(router.urls)),
]
