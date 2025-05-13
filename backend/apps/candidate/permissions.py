from rest_framework.permissions import BasePermission

from apps.user.choices import UserRole
from apps.vacancy.services import VacancyService


class IsHrLeadOrRecruiter(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRole.HR_LEAD or request.user.role == UserRole.RECRUITER


class IsNoteOrReferenceOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.added_by == request.user


class IsVacancyRecruiter(BasePermission):
    def has_permission(self, request, view):
        return VacancyService.get_vacancy_recruiter(request.data.get('vacancy')) == request.user