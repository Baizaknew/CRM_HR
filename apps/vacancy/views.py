from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.user.choices import UserRole
from apps.vacancy.models import Vacancy
from apps.vacancy.permissions import IsHrLeadOrAssignedRecruiter
from apps.vacancy.serializers import VacancyListSerializerForDepartmentHead, \
    VacancyListSerializerForHRandRecruiter, VacancyDetailSerializer, VacancyUpdateSerializerForHrLead, \
    VacancyUpdateSerializerForRecruiter
from apps.vacancy_request.permissions import IsHrLead


@extend_schema(tags=['vacancy'])
class VacancyModelViewSet(ModelViewSet):
    queryset = Vacancy.objects.select_related("department_lead", "status", "recruiter")

    def get_queryset(self):
        if self.request.user.role == UserRole.DEPARTMENT_HEAD:
            return self.queryset.filter(department_lead=self.request.user)
        elif self.request.user.role == UserRole.RECRUITER:
            return self.queryset.filter(recruiter=self.request.user)
        return self.queryset

    def get_serializer_class(self):
        if self.action == "list":
            if self.request.user.role == UserRole.DEPARTMENT_HEAD:
                return VacancyListSerializerForDepartmentHead
            return VacancyListSerializerForHRandRecruiter
        elif self.action in ("update", "partial_update"):
            if self.request.user.role == UserRole.RECRUITER:
                return VacancyUpdateSerializerForRecruiter
            return VacancyUpdateSerializerForHrLead
        return VacancyDetailSerializer

    def get_permissions(self):
        if self.action in ("update", "partial_update", "retrieve"):
            return (IsAuthenticated(), IsHrLeadOrAssignedRecruiter())
        elif self.action == "destroy":
            return (IsAuthenticated(), IsHrLead())
        return (IsAuthenticated(),)
