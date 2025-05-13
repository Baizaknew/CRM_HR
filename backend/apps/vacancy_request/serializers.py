from rest_framework import serializers

from django.contrib.auth import get_user_model

from apps.vacancy_request.models import VacancyRequest, VacancyRequestChangeHistory, VacancyRequestComment

User = get_user_model()


class UserSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class VacancyRequestCreateSerializer(serializers.ModelSerializer):
    requester = UserSimpleSerializer(read_only=True)
    class Meta:
        model = VacancyRequest
        fields = ('id', 'title', 'department', 'city', 'requirements', 'responsibilities', 'min_salary', 'max_salary', 'requester')


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
    vacancy = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = VacancyRequest
        fields = ('id', 'title', 'department', 'city', 'status', 'requester',
                  'requirements', 'responsibilities', 'approver', 'vacancy',
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


class VacancyRequestChangeHistorySerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = VacancyRequestChangeHistory
        fields = ('id', 'user', 'comment', 'created_at')


class VacancyRequestCommentCreateSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = VacancyRequestComment
        fields = ('id', 'text', 'user', 'vacancy_request', 'created_at')


class VacancyRequestCommentSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = VacancyRequestComment
        fields = ('id', 'text', 'user', 'created_at')