from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.user.serializers import UserSerializer
from apps.vacancy_request.permissions import IsHrLead
from apps.user.permissoins import IsUserOrHrLead

User = get_user_model()


@extend_schema(tags=['user'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ('create', 'delete'):
            return (IsHrLead(),)
        elif self.action in ('update', 'partial_update'):
            return (IsUserOrHrLead(),)
        return (IsAuthenticated(),)
