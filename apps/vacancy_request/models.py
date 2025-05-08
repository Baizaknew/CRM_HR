from django.db import models
from django.contrib.auth import get_user_model

from apps.utils.base_models import BaseCommendModel, BaseHistoryChangesModel
from apps.utils.base_models import VacancyBaseModel
from apps.vacancy_request.choices import VacancyRequestStatus

User = get_user_model()


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


class VacancyRequestComment(BaseCommendModel):
    vacancy_request = models.ForeignKey(VacancyRequest, related_name="comments", on_delete=models.SET_NULL,
                                        verbose_name="Заявка на подбор", null=True, blank=True)

    class Meta:
        verbose_name = "Комментарий к Заявке на подбор"
        verbose_name_plural = "Комментарии к Заявкам на подбор"

    def __str__(self):
        return self.text


class VacancyRequestChangeHistory(BaseHistoryChangesModel):
    vacancy_request = models.ForeignKey(
        VacancyRequest,
        related_name="changes",
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    class Meta:
        verbose_name = "История изменений к Заявке на подбор"
        verbose_name_plural = "Истории изменений к Заявкам на подбор"

    def __str__(self):
        return self.comment
