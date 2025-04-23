from django.db.models import TextChoices


class UserRoleChoices(TextChoices):
    DEPARTMENT_HEAD = 'department_head', 'Руководитель'
    HR_LEAD = 'hr_lead', 'Глава HR'
    RECRUITER = 'recruiter', 'Рекрютер'
