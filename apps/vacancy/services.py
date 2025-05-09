from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.exceptions import ValidationError

from apps.vacancy.models import VacancyStatus, Vacancy, VacancyChangeHistory
from apps.vacancy.serializers import VacancyCreateSerializer
from apps.vacancy_request.models import VacancyRequest


User = get_user_model()


class VacancyService:
    """Сервис для Вакансий"""

    @staticmethod
    def log_change(vacancy: Vacancy, user: User, old_status=None, new_status=None, comment=None) -> None:
        """Метод для записи истории изменений"""
        if not comment:
            if old_status and old_status != vacancy.status:
                comment = f"Статус изменен с '{old_status}' на '{vacancy.status}'"
            else:
                comment = f"Обновлена заявка на подбор пользователем: {user}"

        VacancyChangeHistory.objects.create(
            vacancy=vacancy,
            user=user,
            old_status=old_status,
            new_status=new_status,
            comment=comment
        )

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

        if instance.max_salary is not None:
            data['salary'] = f'от {instance.min_salary if instance.min_salary else 0} до {instance.max_salary}'

        serializer = VacancyCreateSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            vacancy_instance = serializer.save()
            return vacancy_instance
        except ValidationError as e:
            # TODO Логирование
            return None

    @staticmethod
    def close_vacancy_as_hired(vacancy: Vacancy) -> Vacancy:
        vacancy.status = VacancyStatus.objects.get(is_closed=True)
        vacancy.closed_at = timezone.now()
        vacancy.save()
        return vacancy

    @staticmethod
    def get_vacancy_recruiter(vacancy_id: int) -> str:
        return Vacancy.objects.get(pk=vacancy_id).recruiter