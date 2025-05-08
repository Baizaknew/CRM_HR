from drf_spectacular.utils import extend_schema
from rest_framework import status

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.user.choices import UserRole
from apps.vacancy.services import VacancyService
from apps.vacancy_request.models import VacancyRequest
from apps.vacancy_request.permissions import IsHrLeadOrDepartmentHead, IsDepartmentHead, IsHrLead, IsOwner, \
    CanEditWhenNeedsRevisions, CanAdminActOnReview, CanResubmitWhenNeedsRevisions
from apps.vacancy_request.serializers import VacancyRequestCreateSerializer, VacancyRequestListSerializer, \
    VacancyRequestDetailSerializer, VacancyRequestResubmitSerializer, VacancyRequestApproveSerializer, \
    VacancyRequestRejectSerializer, VacancyRequestRevisionSerializer, VacancyRequestSendForRevisionSerializer, \
    VacancyRequestChangeHistorySerializer
from apps.vacancy_request.services import VacancyRequestService

@extend_schema(tags=['vacancy-request'])
class VacancyRequestModelViewSet(ModelViewSet):
    queryset = VacancyRequest.objects.select_related('requester', 'approver').all()
    serializer_map = {
        'create': VacancyRequestCreateSerializer,
        'list': VacancyRequestListSerializer,
        'detail': VacancyRequestDetailSerializer,
        'reject': VacancyRequestRejectSerializer,
        'approve': VacancyRequestApproveSerializer,
        'resubmit': VacancyRequestResubmitSerializer,
        'retrieve': VacancyRequestDetailSerializer,
        'send_for_revision': VacancyRequestSendForRevisionSerializer,
        'update': VacancyRequestRevisionSerializer,
        'partial_update': VacancyRequestRevisionSerializer,
        'changes_history': VacancyRequestChangeHistorySerializer,
    }

    def get_queryset(self):
        if self.request.user.role == UserRole.HR_LEAD:
            return self.queryset
        return self.queryset.filter(requester=self.request.user)

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, VacancyRequestDetailSerializer)

    def get_permissions(self):
        if self.action == 'create':
            return (IsDepartmentHead(), IsAuthenticated())
        elif self.action in ('list', 'retrieve', 'changes_history'):
            return (IsHrLeadOrDepartmentHead(), IsAuthenticated())
        elif self.action in ('update', 'partial_update'):
            return (IsDepartmentHead(), CanEditWhenNeedsRevisions(), IsOwner())
        elif self.action in ('approve', 'reject', 'send_for_revision'):
            return (IsHrLead(), CanAdminActOnReview())
        elif self.action == 'resubmit':
            return (IsDepartmentHead(), IsOwner(), CanResubmitWhenNeedsRevisions())
        return (IsHrLeadOrDepartmentHead(), IsAuthenticated(), IsHrLead())


    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        instance = self.get_object()
        updated_instance = VacancyRequestService.approve(instance, request.user)
        created_vacancy = VacancyService.create(instance)
        if created_vacancy is None:
            return Response(
                {'messgae': 'Ошибка при создании вакансии'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        serializer = VacancyRequestDetailSerializer(updated_instance, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        instance = self.get_object()
        serializer = VacancyRequestRejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_instance = VacancyRequestService.reject(
            instance, request.user,
            serializer.validated_data['rejected_reason']
        )

        response_serializer = VacancyRequestDetailSerializer(updated_instance, context={'request': request})
        return Response(response_serializer.data)

    @action(detail=True, methods=['post'], url_path='send-for-revision')
    def send_for_revision(self, request, pk=None):
        instance = self.get_object()
        updated_instance = VacancyRequestService.send_for_revision(instance, request.user)

        serializer = VacancyRequestDetailSerializer(updated_instance, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='resubmit')
    def resubmit(self, request, pk=None):
        instance = self.get_object()
        serializer = VacancyRequestResubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_instance = VacancyRequestService.resubmit(instance, request.user)
        serializer = VacancyRequestDetailSerializer(updated_instance, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='changes-history')
    def changes_history(self, request, pk=None):
        instance = self.get_object()
        history_qs = instance.changes.select_related('user')
        serializer = VacancyRequestChangeHistorySerializer(history_qs, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)
