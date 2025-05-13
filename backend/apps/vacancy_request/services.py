from django.utils import timezone
from django.contrib.auth import get_user_model

from apps.vacancy_request.choices import VacancyRequestStatus
from apps.vacancy_request.models import VacancyRequest, VacancyRequestChangeHistory

User = get_user_model()


class VacancyRequestService:

    @staticmethod
    def log_change(vacancy_request: VacancyRequest, user: User, old_status=None, comment=None) -> None:
        """Метод для записи истории изменений"""
        if not comment:
            if old_status and old_status != vacancy_request.status:
                comment = f"Статус изменен с '{old_status}' на '{vacancy_request.status}'"
            else:
                comment = f"Обновлена заявка на подбор пользователем: {user}"

        VacancyRequestChangeHistory.objects.create(
            vacancy_request=vacancy_request,
            user=user,
            old_status=old_status,
            new_status=vacancy_request.status,
            comment=comment
        )

    @staticmethod
    def set_vacancy_request_attribs(vacancy_request: VacancyRequest, **kwargs):
        """Метод для обновления полей Заявки"""
        for key, value in kwargs.items():
            setattr(vacancy_request, key, value)

        vacancy_request.save(update_fields=[*kwargs.keys()])
        return vacancy_request

    @staticmethod
    def approve(vacancy_request: VacancyRequest, user: User):
        """Метод для согласования Заявки"""
        updated_vacancy_request = VacancyRequestService.set_vacancy_request_attribs(
            vacancy_request,
            status=VacancyRequestStatus.APPROVED,
            approved_at=timezone.now(),
            approver=user
        )
        VacancyRequestService.log_change(
            vacancy_request=updated_vacancy_request,
            user=user,
            old_status=vacancy_request.status,
            comment=f"Заявка одобрена пользователем {user.username}"
        )
        return updated_vacancy_request

    @staticmethod
    def reject(vacancy_request: VacancyRequest, user: User, rejected_reason: str):
        """Метод для отклонения Заявки"""
        updated_vacancy_request = VacancyRequestService.set_vacancy_request_attribs(
            vacancy_request,
            status=VacancyRequestStatus.REJECTED,
            approver=user,
            approved_at=None,
            rejected_reason=rejected_reason,
        )
        VacancyRequestService.log_change(
            vacancy_request=updated_vacancy_request,
            user=user,
            old_status=vacancy_request.status,
            comment=f"Заявка отклонена пользователем {user.username}"
        )
        return updated_vacancy_request

    @staticmethod
    def send_for_revision(vacancy_request: VacancyRequest, user: User):
        """Метод для отправки заявки на доработку"""
        updated_vacancy_request = VacancyRequestService.set_vacancy_request_attribs(
            vacancy_request,
            status=VacancyRequestStatus.NEEDS_REVISION,
            approver=None,
            approved_at=None,
        )
        VacancyRequestService.log_change(
            vacancy_request=updated_vacancy_request,
            user=user,
            old_status=vacancy_request.status,
            comment=f"Заявка отправлена на доработку руководителю пользователем {user.username}"
        )
        return updated_vacancy_request

    @staticmethod
    def resubmit(vacancy_request: VacancyRequest, user: User):
        """Метод для переотправки заявки руководителем, после доработок"""
        updated_vacancy_request = VacancyRequestService.set_vacancy_request_attribs(
            vacancy_request,
            status=VacancyRequestStatus.IN_REVIEW,
            approver=None,
            approved_at=None,
        )
        VacancyRequestService.log_change(
            vacancy_request=updated_vacancy_request,
            user=user,
            old_status=vacancy_request.status,
            comment=f"Заявка отправлена на рассмотрение после доработок пользователем {user.username}"
        )
        return updated_vacancy_request
