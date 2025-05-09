from django.contrib.auth import get_user_model

from apps.candidate.models import CandidateApplicationChangeHistory, CandidateApplication


User = get_user_model()


class CandidateApplicationLoggingService:

    @staticmethod
    def log_status_change(
        application: CandidateApplication, user: User, old_status_name: str | None,
        new_status_name: str, comment: str = ""
    ):
        CandidateApplicationChangeHistory.objects.create(
            application=application,
            user=user,
            old_status=old_status_name if old_status_name else "Не было (создание)",
            new_status=new_status_name,
            comment=comment
        )

    @staticmethod
    def log_creation(application: CandidateApplication, user: User):
        comment_text = f"Кандидат '{application.candidate}' добавлен на вакансию '{application.vacancy.title}'"
        CandidateApplicationLoggingService.log_status_change(
            application=application,
            user=user,
            old_status_name=None,
            new_status_name=str(application.status),
            comment=comment_text
        )