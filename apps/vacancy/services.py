from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.vacancy.models import VacancyStatus, Vacancy
from apps.vacancy.serializers import VacancyCreateSerializer
from apps.vacancy_request.models import VacancyRequest


class VacancyService:
    """Сервис для Вакансий"""

    @staticmethod
    def get_default_status() -> VacancyStatus:
        try:
            return VacancyStatus.objects.get(is_default=True)
        except VacancyStatus.DoesNotExist:
            # TODO Добавить логирование
            raise ValidationError('Отсутствует дефолтный статус для новых вакансий!')

    @staticmethod
    def create(instance: VacancyRequest) -> Vacancy | None:
        """Создает вакансию"""
        data = {
            'title': instance.title,
            'department': instance.department,
            'city': instance.city,
            'requirements': instance.requirements,
            'responsibilities': instance.responsibilities,
            'department_lead': instance.requester.pk,
            'vacancy_request': instance.pk,
            'status': VacancyService.get_default_status().pk,
        }

        if instance.max_salary:
            data['salary'] = f'от {instance.min_salary if instance.min_salary else 0} до {instance.max_salary}'

        serializer = VacancyCreateSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            vacancy_instance = serializer.save()
            return vacancy_instance
        except ValidationError as e:
            # TODO Логирование
            return None
