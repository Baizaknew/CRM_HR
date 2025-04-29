from django.utils import timezone
from django.contrib.auth import get_user_model

from apps.vacancy_request.choices import VacancyRequestStatus
from apps.vacancy_request.models import VacancyRequest

User = get_user_model()


class VacancyRequestService:
    @staticmethod
    def set_vacancy_request_attribs(vacancy_request: VacancyRequest, **kwargs):
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
        return updated_vacancy_request

    @staticmethod
    def send_for_revision(vacancy_request: VacancyRequest):
        """Метод для отправки заявки на доработку"""
        updated_vacancy_request = VacancyRequestService.set_vacancy_request_attribs(
            vacancy_request,
            status=VacancyRequestStatus.NEEDS_REVISION,
            approver=None,
            approved_at=None,
        )
        return updated_vacancy_request

    @staticmethod
    def resubmit(vacancy_request: VacancyRequest):
        """Метод для переотправки заявки руководителем, после доработок"""
        updated_vacancy_request = VacancyRequestService.set_vacancy_request_attribs(
            vacancy_request,
            status=VacancyRequestStatus.IN_REVIEW,
            approver=None,
            approved_at=None,
        )
        return updated_vacancy_request