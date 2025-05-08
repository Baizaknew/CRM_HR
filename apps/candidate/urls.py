from rest_framework.routers import DefaultRouter

from django.urls import path, include

from apps.candidate.views import CandidateModelViewSet, CandidateApplicationViewSet, \
    CandidateApplicationStatusViewSet, CandidateSourceViewSet, CandidateTagViewSet, CandidateNoteViewSet, \
    CandidateReferenceViewSet


candidate_router = DefaultRouter()
candidate_router.register('profiles', CandidateModelViewSet, basename='candidate-profile')

application_router = DefaultRouter()
application_router.register('applications', CandidateApplicationViewSet, basename='candidate-application')

misc_router = DefaultRouter()
misc_router.register('application-statuses', CandidateApplicationStatusViewSet, basename='candidate-application-status')
misc_router.register('tags', CandidateTagViewSet, basename='candidate-application-tag')
misc_router.register('sources', CandidateSourceViewSet, basename='candidate-application-source')
misc_router.register('notes', CandidateNoteViewSet, basename='candidate-note')
misc_router.register('references', CandidateReferenceViewSet, basename='candidate-reference')


urlpatterns = [
    path('candidates/', include(candidate_router.urls)),
    path('candidates/', include(application_router.urls)),
    path('candidates/', include(misc_router.urls))
]
