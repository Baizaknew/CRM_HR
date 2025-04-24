from apps.vacancy.models import VacancyStatus


def get_default_vacancy_status_pk():
    return VacancyStatus.objects.get(is_default=True).pk
