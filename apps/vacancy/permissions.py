from rest_framework.permissions import BasePermission

from apps.user.choices import UserRole


class IsAssignedRecruiter(BasePermission):
    """Доступ для редактирования только своих вакансий"""
    message = "Вы можете редактировать только свои Вакансии"
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.recruiter


class IsRecruiter(BasePermission):
    """Доступ только рекрутеру"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.RECRUITER
