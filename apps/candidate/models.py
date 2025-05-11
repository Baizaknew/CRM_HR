from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

from apps.candidate.choices import Experience, SourceType
from apps.utils.base_models import BaseModel, BaseStatusModel, BaseHistoryChangesModel
from apps.vacancy.choices import City
from apps.vacancy.models import Vacancy


User = get_user_model()


class CandidateTag(BaseModel):
    title = models.CharField("Название", max_length=100, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.title


class CandidateNote(BaseModel):
    text = models.TextField("Заметка")
    candidate = models.ForeignKey("Candidate", on_delete=models.CASCADE, verbose_name="Кандидат")
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name="Добавил",
        related_name="notes",
    )

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"

    def __str__(self):
        return self.text


class CandidateReference(BaseModel):
    text = models.TextField("Текст")
    candidate = models.ForeignKey("Candidate", on_delete=models.CASCADE, verbose_name="Кандидат")
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name="Добавил",
        related_name="references",
    )
    class Meta:
        verbose_name = "Обратная связь по кандидату"
        verbose_name_plural = "Обратная связь по кандидатам"

    def __str__(self):
        return self.text


class CandidateApplicationStatus(BaseStatusModel):
    is_rejected = models.BooleanField("Статус означает отказ кандидату?", default=False)
    is_success = models.BooleanField("Статус означает, что успешный найм?", default=False)
    is_default = models.BooleanField("Статус по умолчанию", default=False)
    order = models.IntegerField("Очередность", unique=True)

    class Meta:
        verbose_name = "Статус кандидата в вакансии"
        verbose_name_plural = 'Статусы кандидата в вакансии'

    def __str__(self):
        return self.name


class CandidateSource(BaseModel):
    name = models.CharField(
        "Источник", max_length=100,
        help_text="Например: hh.ru, linkedin",
        blank=True, null=True
    )

    class Meta:
        verbose_name = "Источник"
        verbose_name_plural = "Источник"

    def __str__(self):
        return self.name


class CandidateApplication(BaseModel):
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        verbose_name="Вакансия",
        related_name="applications",
    )
    candidate = models.ForeignKey(
        "Candidate",
        on_delete=models.CASCADE,
        verbose_name="Кандидат",
        related_name="applications",
    )
    status = models.ForeignKey(
        CandidateApplicationStatus,
        on_delete=models.PROTECT,
        verbose_name="Статус",
        related_name="applications",
    )
    recruiter = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name="Рекрутер",
        related_name="candidate_applications",
    )
    rejected_reason = models.CharField("Причина отказа", max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Заявка кандидата на вакансию"
        verbose_name_plural = "Заявки кандидатов на вакансии"
        unique_together = ("candidate", "vacancy")

    def __str__(self):
        return f"{self.candidate.first_name} - {self.vacancy.title}"


class Candidate(BaseModel):
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    patronymic = models.CharField("Отчество", max_length=100, blank=True, null=True)
    resume = models.FileField("Резюме", upload_to="resume", blank=True, null=True)

    city = models.CharField("Локация", choices=City.choices, max_length=50, blank=True, null=True)
    experience = models.CharField("Опыт", choices=Experience.choices, max_length=100)
    phone_number = models.CharField("Номер телефона", max_length=20, blank=True, null=True)
    email = models.EmailField("Почта", blank=True, null=True)
    cover_letter = models.TextField("Сопроводительное письмо", blank=True, null=True)
    tags = models.ManyToManyField(CandidateTag, verbose_name="Теги")
    vacancy = models.ManyToManyField(Vacancy, through=CandidateApplication)
    salary_expectation = models.CharField("Зарплатные ожидания", max_length=100, blank=True, null=True)
    source = models.ForeignKey(
        CandidateSource,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name="Источник"
    )
    source_type = models.CharField(
        "Тип отклика",
        choices=SourceType.choices,
        max_length=50,
        blank=True, null=True
    )
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name="Добавлен пользователем"
    )

    class Meta:
        verbose_name = "Кандидат"
        verbose_name_plural = "Кандидаты"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return f"{settings.FRONTEND_BASE_URL}{reverse('candidate-profile-detail', kwargs={'pk': self.pk})}"

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'


class CandidateApplicationChangeHistory(BaseHistoryChangesModel):
    application = models.ForeignKey(
        CandidateApplication,
        related_name="changes",
        on_delete=models.CASCADE,
        verbose_name="Заявка кандидата",
    )

    class Meta:
        verbose_name = "История изменения статуса заявки"
        verbose_name_plural = "История изменения статусов заявок"

    def __str__(self):
        return self.comment
