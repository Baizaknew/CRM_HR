from django.db import models
from django.contrib.auth import get_user_model

from ckeditor.fields import RichTextField

from apps.utils.base_model import BaseModel
from apps.vacancy.choices import Department, City, Priority

User = get_user_model()


def get_default_vacancy_status_pk():
    """Возвращает дефолтный статус для Вакансии при создании."""
    try:
        status = VacancyStatus.objects.get(is_default=True)
        return status.pk
    except VacancyStatus.DoesNotExist:
        return None


class VacancyStatus(BaseModel):
    name = models.CharField("Статус", max_length=100)
    is_default = models.BooleanField("Статус по умолчанию", default=False)

    class Meta:
        verbose_name = "Статус вакансии"
        verbose_name_plural = "Статусы вакансий"

    def __str__(self):
        return self.name


class Vacancy(BaseModel):
    title = models.CharField("Название", max_length=255)
    department = models.CharField("Отдел", choices=Department.choices, max_length=255)
    city = models.CharField("Город", choices=City.choices, max_length=255)
    priority = models.CharField("Приоритет", choices=Priority.choices, max_length=255)
    status = models.ForeignKey(VacancyStatus, related_name="vacancies", on_delete=models.CASCADE,
                               verbose_name="Статус", default=get_default_vacancy_status_pk())
    department_lead = models.ForeignKey(User, related_name="dl_vacancies", on_delete=models.CASCADE,
                               verbose_name="Руководитель")
    recruiter = models.ForeignKey(User, related_name="rc_vacancies", on_delete=models.CASCADE,
                               verbose_name="Рекрутер")
    requirements = RichTextField("Требования к кандидату")
    responsibilities = RichTextField("Обязанности кандидата")
    min_salary = models.IntegerField("Минимальная зарплата")
    max_salary = models.IntegerField("Максимальная зарплата")

    opened_at = models.DateTimeField("Дата открытия", blank=True, null=True)
    closed_at = models.DateTimeField("Дата закрытия", blank=True, null=True)
    time_to_offer = models.DurationField("Понадобившееся время", blank=True, null=True)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.title