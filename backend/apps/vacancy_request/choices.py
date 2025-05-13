from django.db.models import TextChoices


class VacancyRequestStatus(TextChoices):
    IN_REVIEW = 'IN_REVIEW', 'На рассмотрении'
    NEEDS_REVISION = 'NEEDS_REVISION', 'Требует доработки'
    APPROVED = 'APPROVED', 'Одобрено'
    REJECTED = 'REJECTED', 'Отклонено'
