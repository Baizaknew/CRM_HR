from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from rest_framework import status, viewsets, filters

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.user.choices import UserRole
from apps.utils.tasks import send_email_notification, send_telegram_notification
from apps.vacancy.services import VacancyService
from apps.vacancy_request.models import VacancyRequest, VacancyRequestComment
from apps.vacancy_request.permissions import IsCommentOwner, IsHrLeadOrDepartmentHead, IsDepartmentHead, IsHrLead, IsOwner, \
    CanEditWhenNeedsRevisions, CanAdminActOnReview, CanResubmitWhenNeedsRevisions
from apps.vacancy_request.serializers import VacancyRequestCreateSerializer, VacancyRequestListSerializer, \
    VacancyRequestDetailSerializer, VacancyRequestResubmitSerializer, VacancyRequestApproveSerializer, \
    VacancyRequestRejectSerializer, VacancyRequestRevisionSerializer, VacancyRequestSendForRevisionSerializer, \
    VacancyRequestChangeHistorySerializer, VacancyRequestCommentCreateSerializer, VacancyRequestCommentSerializer
from apps.vacancy_request.services import VacancyRequestService


User = get_user_model()


@extend_schema(tags=['vacancy-request'])
class VacancyRequestModelViewSet(viewsets.ModelViewSet):
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['requester', 'status', 'department', 'city']
    search_fields = ['title']

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
        instance = serializer.save(requester=self.request.user)
        send_email_notification.delay(
            "Новая заявка на подбор",
            [user.email for user in User.objects.filter(role=UserRole.HR_LEAD)],
            {"manager_name": self.request.user.username, "vacancy_request_url": instance.get_absolute_url()},
            "creating_vacancy_request.html"
        )
        send_telegram_notification.delay(
            f"Новая заявка на подбор от руководителя {self.request.user.username}",
        )


@extend_schema(tags=['vacancy-request-comments'])
class VacancyRequestCommentViewSet(viewsets.ModelViewSet):
    queryset = VacancyRequestComment.objects.all()
    permission_classes = (IsAuthenticated, IsHrLeadOrDepartmentHead, IsCommentOwner)

    def get_serializer_class(self):
        if self.action == 'create':
            return VacancyRequestCommentCreateSerializer
        return VacancyRequestCommentSerializer

    def get_queryset(self):
        if self.action == 'list':
            vacancy_request_id = self.request.query_params.get('vacancy_request_id')
            if vacancy_request_id:
                return self.queryset.filter(vacancy_request_id=vacancy_request_id)
        return self.queryset

    @extend_schema(parameters=[
        OpenApiParameter(name='vacancy_request_id', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, required=True),
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
