from django.db.models import TextChoices


class Experience(TextChoices):
    JUNIOR = 'JUNIOR', 'Младший'
    MIDDLE = 'MIDDLE', 'Средний'
    SENIOR = 'SENIOR', 'Профессионал'


class SourceType(TextChoices):
    APPLICATION = 'APPLICATION', 'Отклик на вакансию'
    SOURCED = 'SOURCED', 'Найден рекрутером'
    REFERRAL = 'REFERRAL', 'Рекомендация'
    INTERNAL = 'INTERNAL', 'Внутренний кандидат'
    UNSOLICITED = 'UNSOLICITED', 'Самостоятельное обращение'
    OTHER = 'OTHER', 'Другое'
