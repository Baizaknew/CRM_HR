from django.db import models
from django.contrib.auth import get_user_model

from ckeditor.fields import RichTextField

from apps.utils.base_models import BaseModel, BaseCommendModel
from apps.vacancy.choices import Department, City, Priority, VacancyRequestStatus

User = get_user_model()


class VacancyBaseModel(BaseModel):
    title = models.CharField("Название", max_length=255)
    department = models.CharField("Отдел", choices=Department.choices, max_length=50)
    city = models.CharField("Город", choices=City.choices, max_length=50)
    requirements = RichTextField("Требования к кандидату")
    responsibilities = RichTextField("Обязанности кандидата")

    class Meta:
        abstract = True


class VacancyStatus(BaseModel):
    name = models.CharField("Статус", max_length=100, unique=True)
    is_default = models.BooleanField("Статус по умолчанию", default=False)

    class Meta:
        verbose_name = "Статус вакансии"
        verbose_name_plural = "Статусы вакансий"

    def __str__(self):
        return self.name


class VacancyRequest(VacancyBaseModel):
    """Модель для - Заявки на подбор"""
    requester = models.ForeignKey(User, related_name="vacancy_requests", on_delete=models.PROTECT,
                                  verbose_name="Отправитель")
    approver = models.ForeignKey(User, related_name="vacancy_approvers", on_delete=models.SET_NULL,
                                 blank=True, null=True, verbose_name="Согласующий")
    rejected_reason = models.CharField("Причина отклонения", max_length=500, blank=True, null=True)
    status = models.CharField("Статус", choices=VacancyRequestStatus.choices, max_length=50,
                              default=VacancyRequestStatus.IN_REVIEW)
    approved_at = models.DateTimeField("Дата согласования HR", null=True, blank=True)
    min_salary = models.IntegerField("Минимальная зарплата", null=True, blank=True)
    max_salary = models.IntegerField("Максимальная зарплата", null=True, blank=True)

    class Meta:
        verbose_name = "Заявка на подбор"
        verbose_name_plural = "Заявки на подбор"
        ordering = ('-created_at',)

    def __str__(self):
        return f"Заявка от {self.requester.username}"


class Vacancy(VacancyBaseModel):
    priority = models.CharField("Приоритет", choices=Priority.choices, max_length=50, default=Priority.MEDIUM)
    status = models.ForeignKey(VacancyStatus, related_name="vacancies", on_delete=models.PROTECT,
                               verbose_name="Статус",)# default=get_default_vacancy_status_pk())
    department_lead = models.ForeignKey(User, related_name="dl_vacancies", on_delete=models.PROTECT,
                               verbose_name="Руководитель отдела")
    recruiter = models.ForeignKey(User, related_name="rc_vacancies", on_delete=models.SET_NULL,
                               verbose_name="Рекрутер", null=True, blank=True)
    salary = models.CharField("Зарплата (текст)", max_length=255, blank=True, null=True)
    vacancy_request = models.OneToOneField(VacancyRequest, related_name="vacancy", on_delete=models.PROTECT,
                                           verbose_name="Исходная заявка")

    opened_at = models.DateTimeField("Дата открытия (взятия в работу)", blank=True, null=True)
    closed_at = models.DateTimeField("Дата закрытия", blank=True, null=True)
    time_to_offer = models.DurationField("Время до оффера", blank=True, null=True)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ('-created_at', 'priority',)

    def __str__(self):
        return self.title


class VacancyRequestComment(BaseCommendModel):
    vacancy_request = models.ForeignKey(VacancyRequest, related_name="comments", on_delete=models.SET_NULL,
                                        verbose_name="Заявка на подбор", null=True, blank=True)


class VacancyComment(BaseCommendModel):
    vacancy = models.ForeignKey(Vacancy, related_name="comments", on_delete=models.SET_NULL,
                                verbose_name="Вакансия", null=True, blank=True)
