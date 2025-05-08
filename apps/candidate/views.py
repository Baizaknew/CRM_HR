from django.db.models import Prefetch
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.candidate.models import Candidate, CandidateApplication, CandidateNote, CandidateReference, \
    CandidateApplicationStatus, CandidateSource, CandidateTag
from apps.candidate.permissions import IsHrLeadOrRecruiter, IsNoteOrReferenceOwner
from apps.candidate.serializers import CandidateListSerializer, CandidateUpdateCreateSerializer, \
    CandidateReferencesListDetailSerializer, CandidateNoteCreateSerializer, \
    CandidateReferenceCreateSerializer, CandidateApplicationSerializer, CandidateApplicationStatusSerializer, \
    CandidateApplicationUpdateSerializer, CandidateSourceSerializer, CandidateTagSerializer, \
    CandidateReferenceUpdateSerializer, CandidateNoteUpdateSerializer, CandidateNoteListDetailSerializer, CandidateDetailSerializer
from apps.vacancy.services import VacancyService
from apps.vacancy_request.permissions import IsHrLead


@extend_schema(tags=['candidate'])
class CandidateModelViewSet(ModelViewSet):

    queryset = Candidate.objects.select_related('source', 'added_by').prefetch_related(
        'tags',
        Prefetch(
            'applications',
            queryset=CandidateApplication.objects.select_related('vacancy','status',).order_by('-created_at'),
        )
    )
    permission_classes = (IsAuthenticated, IsHrLeadOrRecruiter,)

    def get_serializer_class(self):
        if self.action == 'list':
            return CandidateListSerializer
        elif self.action == 'retrieve':
            return CandidateDetailSerializer
        return CandidateUpdateCreateSerializer

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


@extend_schema(tags=['candidate-applications'])
class CandidateApplicationViewSet(ModelViewSet):
    queryset = CandidateApplication.objects.select_related('recruiter', 'status')
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.action == 'list':
            vacancy_id = self.kwargs.get('vacancy_id')
            if vacancy_id:
                return self.queryset.filter(vacancy_id=vacancy_id)
        return self.queryset

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return CandidateApplicationUpdateSerializer
        return CandidateApplicationSerializer

    def get_initial_status(self):
        initial_status = CandidateApplicationStatus.objects.order_by('order').first()
        if initial_status is None:
            raise ValidationError('Ошибка сервера! Не настроен изначальный статус для кандидатов')
        return initial_status

    def perform_create(self, serializer):
        serializer.save(
            recruiter=self.request.user,
            status=self.get_initial_status(),
        )

    def perform_update(self, serializer):
        new_status = serializer.validated_data.get('status')
        updated_application = serializer.save()

        if new_status and new_status.is_success:
            try:
                VacancyService.close_vacancy_as_hired(updated_application.vacancy)
            except Exception as e:
                raise ValidationError({"detail": f"Статус кандидата обновлен, но ошибка при закрытии вакансии: {e}"})

    @extend_schema(parameters=[OpenApiParameter(name='vacancy_id', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY)])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=['candidate-application-status'])
class CandidateApplicationStatusViewSet(ModelViewSet):
    queryset = CandidateApplicationStatus.objects.all()
    serializer_class = CandidateApplicationStatusSerializer

    def get_permissions(self):
        if self.action == 'list':
            return (IsAuthenticated(),)
        return (IsHrLead(),)


@extend_schema(tags=['candidate-sources'])
class CandidateSourceViewSet(ModelViewSet):
    queryset = CandidateSource.objects.all()
    serializer_class = CandidateSourceSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'delete'):
            return (IsHrLead(),)
        return (IsAuthenticated(),)


@extend_schema(tags=['candidate-tags'])
class CandidateTagViewSet(ModelViewSet):
    queryset = CandidateTag.objects.all()
    serializer_class = CandidateTagSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'delete'):
            return (IsHrLead(),)
        return (IsAuthenticated(),)


@extend_schema(tags=['candidate-references'])
class CandidateReferenceViewSet(ModelViewSet):
    queryset = CandidateReference.objects.select_related('added_by').order_by('-created_at')
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'create':
            return CandidateReferenceCreateSerializer
        elif self.action in ('update', 'partial_update'):
            return CandidateReferenceUpdateSerializer
        return CandidateReferencesListDetailSerializer

    def get_queryset(self):
        candidate_id = self.kwargs.get('candidate_id')
        return self.queryset.filter(candidate_id=candidate_id) if candidate_id else self.queryset

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'delete'):
            return (IsNoteOrReferenceOwner(),)
        return (IsAuthenticated(),)

    @extend_schema(parameters=[OpenApiParameter(name='candidate_id', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


@extend_schema(tags=['candidate-notes'])
class CandidateNoteViewSet(ModelViewSet):
    queryset = CandidateNote.objects.select_related('added_by').order_by('-created_at')
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'create':
            return CandidateNoteCreateSerializer
        elif self.action in ('update', 'partial_update'):
            return CandidateNoteUpdateSerializer
        return CandidateNoteListDetailSerializer

    def get_queryset(self):
        candidate_id = self.kwargs.get('candidate_id')
        return self.queryset.filter(candidate_id=candidate_id) if candidate_id else self.queryset

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'delete'):
            return (IsNoteOrReferenceOwner(),)
        return (IsAuthenticated(),)

    @extend_schema(parameters=[OpenApiParameter(name='candidate_id', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)
