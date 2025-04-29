from rest_framework import serializers

from django.contrib.auth import get_user_model

from apps.vacancy.models import VacancyRequest


User = get_user_model()


class UserSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class VacancyRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacancyRequest
        fields = ('id', 'title', 'department', 'city', 'requirements', 'responsibilities', 'min_salary', 'max_salary',)


class VacancyRequestListSerializer(serializers.ModelSerializer):
    requester = UserSimpleSerializer(read_only=True)
    approver = UserSimpleSerializer(read_only=True)

    class Meta:
        model = VacancyRequest
        fields = ('id', 'title', 'department', 'city', 'status', 'requester', 'approver', 'rejected_reason',
                  'created_at', 'updated_at', 'approved_at')


class VacancyRequestDetailSerializer(serializers.ModelSerializer):
    requester = UserSimpleSerializer(read_only=True)
    approver = UserSimpleSerializer(read_only=True)
    class Meta:
        model = VacancyRequest
        fields = ('id', 'title', 'department', 'city', 'status', 'requester',
                  'requirements', 'responsibilities', 'approver',
                  'rejected_reason', 'created_at', 'updated_at', 'approved_at', 'min_salary', 'max_salary')


class VacancyRequestRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacancyRequest
        fields = ('id', 'title', 'department', 'city', 'requirements', 'responsibilities',
                  'min_salary', 'max_salary')
        read_only_fields = ('status', 'requester', 'approver', 'rejected_reason', 'approved_at')


class VacancyRequestApproveSerializer(serializers.Serializer):
    pass


class VacancyRequestRejectSerializer(serializers.Serializer):
    rejected_reason = serializers.CharField(
        required=True,
        max_length=500,
        allow_blank=False,
        error_messages={
            'required': 'Необходимо указать причину отклоенения',
            'blank': 'Причина отклонения не может быть пустой'
        }
    )


class VacancyRequestSendForRevisionSerializer(serializers.Serializer):
    pass


class VacancyRequestResubmitSerializer(serializers.Serializer):
    pass
