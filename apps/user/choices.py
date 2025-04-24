from django.db.models import TextChoices


class UserRole(TextChoices):
    DEPARTMENT_HEAD = 'DEPARTMENT_LEAD', 'Руководитель'
    HR_LEAD = 'HR_LEAD', 'Глава HR'
    RECRUITER = 'RECRUITER', 'Рекрутер'
