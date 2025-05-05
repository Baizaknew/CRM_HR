from django.db import models
from django.contrib.auth import get_user_model


from apps.utils.base_models import BaseModel, BaseCommendModel, VacancyBaseModel, BaseStatusModel
from apps.vacancy.choices import Priority
from apps.vacancy_request.models import VacancyRequest

User = get_user_model()


class VacancyStatus(BaseStatusModel):
    is_default = models.BooleanField("Статус по умолчанию", default=False)
    is_opened = models.BooleanField("Статус активной работы?", default=False,
                                    help_text="Отметьте, если этот статус означает начало активной работы по вакансии "
                                              "(для установки даты `opened_at`)")
    is_closed = models.BooleanField("Финальный (закрытый) статус?", default=False,
                                    help_text="Отметьте, если этот статус завершает работу по вакансии (найм/отмена) и "
                                              "требует установки даты закрытия (`closed_at`)")

    class Meta:
        verbose_name = "Статус вакансии"
        verbose_name_plural = "Статусы вакансий"

    def __str__(self):
        return self.name


class Vacancy(VacancyBaseModel):
    priority = models.CharField("Приоритет", choices=Priority.choices, max_length=50, default=Priority.MEDIUM)
    status = models.ForeignKey(VacancyStatus, related_name="vacancies", on_delete=models.PROTECT,
                               verbose_name="Статус",)
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


class VacancyComment(BaseCommendModel):
    vacancy = models.ForeignKey(Vacancy, related_name="comments", on_delete=models.SET_NULL,
                                verbose_name="Вакансия", null=True, blank=True)
