from rest_framework import serializers

from apps.vacancy.models import Vacancy, VacancyChangeHistory, VacancyComment
from apps.vacancy_request.serializers import UserSimpleSerializer


class SimpleVacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ('id', 'title',)


class VacancyListSerializerForHRandRecruiter(serializers.ModelSerializer):
    recruiter = UserSimpleSerializer(read_only=True)
    department_lead = UserSimpleSerializer(read_only=True)
    class Meta:
        model = Vacancy
        fields = ('id', 'title', 'department', 'city', 'priority', 'created_at', 'updated_at', 'status',
                  'opened_at', 'closed_at', 'recruiter', 'department_lead', 'time_to_offer')


class VacancyListSerializerForDepartmentHead(serializers.ModelSerializer):
    recruiter = UserSimpleSerializer(read_only=True)
    department_lead = UserSimpleSerializer(read_only=True)
    class Meta:
        model = Vacancy
        fields = ('id', 'title', 'priority', 'created_at', 'updated_at', 'status',
                  'opened_at', 'closed_at', 'recruiter', 'department_lead', 'time_to_offer')


class VacancyDetailSerializer(serializers.ModelSerializer):
    recruiter = UserSimpleSerializer(read_only=True)
    department_lead = UserSimpleSerializer(read_only=True)
    class Meta:
        model = Vacancy
        fields = ('id', 'title', 'department', 'city', 'requirements', 'responsibilities', 'priority', 'created_at',
                  'updated_at', 'status', 'opened_at', 'closed_at', 'recruiter', 'department_lead', 'time_to_offer',
                  'salary',)


class VacancyUpdateSerializerForHrLead(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ('id', 'title', 'department', 'city', 'requirements', 'responsibilities', 'priority',
                  'status', 'recruiter', 'department_lead',
                  'salary',)


class VacancyUpdateSerializerForRecruiter(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ('id', 'title', 'department', 'city', 'requirements', 'responsibilities',
                  'status', 'salary',)


class VacancyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ('title', 'department', 'city', 'requirements', 'responsibilities',
                  'department_lead', 'vacancy_request', 'status', 'salary',)


class VacancyChangeHistorySerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = VacancyChangeHistory
        fields = ('id', 'user', 'comment', 'created_at')


class VacancyCommentCreateSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = VacancyComment
        fields = ('id', 'text', 'user', 'vacancy', 'created_at')


class VacancyCommentSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = VacancyComment
        fields = ('id', 'text', 'user', 'created_at')
