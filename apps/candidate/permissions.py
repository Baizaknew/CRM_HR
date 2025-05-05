from rest_framework.permissions import BasePermission

from apps.user.choices import UserRole


class IsHrLeadOrRecruiter(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRole.HR_LEAD or request.user.role == UserRole.RECRUITER