from rest_framework.permissions import BasePermission

from apps.user.choices import UserRole


class IsHrLeadOrDepartmentHead(BasePermission):
    def has_permission(self, request, view):
        if request.user.role in (UserRole.HR_LEAD, UserRole.DEPARTMENT_HEAD):
            return True
        return False
