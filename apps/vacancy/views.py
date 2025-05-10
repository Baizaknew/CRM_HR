from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.candidate.models import CandidateApplicationChangeHistory
from apps.user.choices import UserRole
from apps.vacancy.models import Vacancy, VacancyChangeHistory, VacancyComment
from apps.vacancy.permissions import IsHrLeadOrAssignedRecruiter, IsVacancyOwner
from apps.vacancy.serializers import (VacancyListSerializerForDepartmentHead,
                                      VacancyListSerializerForHRandRecruiter,
                                      VacancyDetailSerializer,
                                      VacancyUpdateSerializerForHrLead,
                                      VacancyUpdateSerializerForRecruiter, VacancyChangeHistorySerializer,
                                      VacancyCommentCreateSerializer, VacancyCommentSerializer)
from apps.vacancy.services import VacancyService
from apps.vacancy_request.permissions import IsHrLead


@extend_schema(tags=['vacancy'])
class VacancyModelViewSet(ModelViewSet):
    queryset = Vacancy.objects.select_related("department_lead", "status", "recruiter")

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.queryset.none()
        elif self.request.user.role == UserRole.DEPARTMENT_HEAD:
            return self.queryset.filter(department_lead=self.request.user)
        elif self.request.user.role == UserRole.RECRUITER:
            return self.queryset.filter(recruiter=self.request.user)
        return self.queryset

    def get_serializer_class(self):
        if self.action == "list":
            if self.request.user.is_authenticated and self.request.user.role == UserRole.DEPARTMENT_HEAD:
                return VacancyListSerializerForDepartmentHead
            return VacancyListSerializerForHRandRecruiter
        elif self.action in ("update", "partial_update"):
            if self.request.user.is_authenticated and self.request.user.role == UserRole.RECRUITER:
                return VacancyUpdateSerializerForRecruiter
            return VacancyUpdateSerializerForHrLead
        return VacancyDetailSerializer

    def get_permissions(self):
        if self.action in ("update", "partial_update",):
            return (IsAuthenticated(), IsHrLeadOrAssignedRecruiter(),)
        elif self.action == "destroy":
            return (IsAuthenticated(), IsHrLead())
        elif self.action == "retrieve":
            return (IsAuthenticated(), IsVacancyOwner(),)
        return (IsAuthenticated(),)

    def perform_update(self, serializer):
        instance = serializer.instance
        validated_data = serializer.validated_data
        new_status = validated_data.get('status')

        save_kwargs = {}

        if new_status:
            VacancyService.log_change(
                vacancy=instance,
                user=self.request.user,
                old_status=instance.status,
                new_status=new_status,
                comment=f"Пользователь {self.request.user} поменял статус вакансии с {instance.status} на {new_status}"
            )
            if new_status.is_closed:
                if not instance.status or not instance.status.is_closed:
                    instance.closed_at = timezone.now()
                    save_kwargs['closed_at'] = timezone.now()
            elif new_status.is_opened:
                if not instance.status or not instance.status.is_opened:
                    instance.opened_at = timezone.now()
                    save_kwargs['opened_at'] = timezone.now()

        super().perform_update(serializer)

    @action(detail=True, methods=['get'], url_path='activity-log')
    def activity_log(self, request, pk=None):
        instance = self.get_object()

        histories = CandidateApplicationChangeHistory.objects.filter(application__vacancy=instance).order_by('-created_at')

        serializer = VacancyChangeHistorySerializer(histories, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='changes-history')
    def changes_history(self, request, pk=None):
        instance = self.get_object()
        histories = instance.changes.select_related('user')
        serializer = VacancyChangeHistorySerializer(histories, many=True)
        return Response(serializer.data)

@extend_schema(tags=['vacancy-comments'])
class VacancyCommentViewSet(ModelViewSet):
    queryset = VacancyComment.objects.all()
    permission_classes = (IsAuthenticated, IsVacancyOwner)

    def get_serializer_class(self):
        if self.action == 'create':
            return VacancyCommentCreateSerializer
        return VacancyCommentSerializer

    def get_queryset(self):
        print('!AAAAAaa')
        if self.action == 'list':
            vacancy_id = self.request.query_params.get('vacancy_id')
            print('sad')
            if vacancy_id:
                return self.queryset.filter(vacancy_id=vacancy_id)
        return self.queryset

    @extend_schema(parameters=[
        OpenApiParameter(name='vacancy_id', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, required=True),
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )
