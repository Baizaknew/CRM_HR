from django.db.models import TextChoices


class UserRoleChoices(TextChoices):
    DEPARTMENT_HEAD = 'DEPARTMENT_LEAD', 'Руководитель'
    HR_LEAD = 'HR_LEAD', 'Глава HR'
    RECRUITER = 'RECRUITER', 'Рекрутер'
