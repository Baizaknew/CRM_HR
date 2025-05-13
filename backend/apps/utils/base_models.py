from django.db import models
from django.contrib.auth import get_user_model

from apps.vacancy.choices import Department, City

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseCommendModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Пользователь", blank=True, null=True)
    text = models.TextField("Комментарий")

    class Meta:
        abstract = True
        ordering = ('-created_at',)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text


class VacancyBaseModel(BaseModel):
    title = models.CharField("Название", max_length=255)
    department = models.CharField("Отдел", choices=Department.choices, max_length=50)
    city = models.CharField("Город", choices=City.choices, max_length=50)
    requirements = models.TextField("Требования к кандидату")
    responsibilities = models.TextField("Обязанности кандидата")

    class Meta:
        abstract = True


class BaseStatusModel(BaseModel):
    name = models.CharField("Статус", max_length=100, unique=True)

    class Meta:
        abstract = True


class BaseHistoryChangesModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Пользователь")
    old_status = models.CharField("Старый статус", max_length=50, blank=True, null=True)
    new_status = models.CharField("Новый статус", max_length=50, blank=True, null=True)
    comment = models.CharField("Комментарий", max_length=500)

    class Meta:
        abstract = True
