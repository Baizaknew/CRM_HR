from rest_framework.permissions import BasePermission

from apps.user.choices import UserRole
from apps.vacancy_request.choices import VacancyRequestStatus


class IsHrLeadOrDepartmentHead(BasePermission):
    """Доступ HR главе и руководителю"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in (UserRole.HR_LEAD, UserRole.DEPARTMENT_HEAD)


class IsHrLead(BasePermission):
    """Доступ главе HR"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.HR_LEAD


class IsDepartmentHead(BasePermission):
    """Доступ руководителю"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.DEPARTMENT_HEAD


class IsOwner(BasePermission):
    """Доступ владельцу заявки"""
    def has_object_permission(self, request, view, obj):
        return obj.requester == request.user and request.user.is_authenticated


class CanEditWhenNeedsRevisions(BasePermission):
    """Доступ руководителю к редактированию, если статус объекта - NEEDS_REVISION"""
    message = "Руководитель может редактировать, только если статус Заявки - 'Требует доработки'"
    def has_object_permission(self, request, view, obj):
        return obj.status == VacancyRequestStatus.NEEDS_REVISION


class CanResubmitWhenNeedsRevisions(CanEditWhenNeedsRevisions):
    """Тоже самое, что и CanEditWhenNeedsRevisions, новый класс для ясности в названии"""
    pass


class CanAdminActOnReview(BasePermission):
    """Доступ HR на изменение статуса, только если Заявка со статусом - 'На рассмотрении'"""
    message = "Разрешено если статус Заявки - 'На рассмотрении'"
    def has_object_permission(self, request, view, obj):
        return obj.status == VacancyRequestStatus.IN_REVIEW
