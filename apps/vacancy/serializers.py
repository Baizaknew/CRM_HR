from rest_framework import serializers

from apps.vacancy.models import VacancyRequest


class VacancyRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacancyRequest
        fields = ('title', 'department', 'city', 'requirements', 'responsibilities')
