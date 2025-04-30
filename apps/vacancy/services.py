from django.forms import model_to_dict

from apps.vacancy.models import VacancyStatus
from apps.vacancy.serializers import VacancyCreateSerializer
from apps.vacancy_request.models import VacancyRequest


class VacancyService:
    """Сервис для Вакансий"""

    @staticmethod
    def get_default_status() -> VacancyStatus:
        try:
            return VacancyStatus.objects.get(is_default=True).status
        except VacancyStatus.DoesNotExist:
            return VacancyStatus.objects.create(is_default=True, name="На рассмотрении")


    @staticmethod
    def create(instance: VacancyRequest) -> VacancyCreateSerializer:
        """Создает вакансию"""
        data = {
            'title': instance.title,
            'department': instance.department,
            'city': instance.city,
            'requirements': instance.requirements,
            'responsibilities': instance.responsibilities,
            'department_lead': instance.requester.pk,
            'vacancy_request': instance.pk,
            'status': VacancyService.get_default_status(),
            'salary': f'от {instance.min_salary} до {instance.max_salary}',
        }
        serializer = VacancyCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return serializer
