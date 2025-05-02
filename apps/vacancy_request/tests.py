from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.vacancy.choices import City, Department
from apps.vacancy_request.choices import VacancyRequestStatus
from apps.vacancy_request.models import VacancyRequest
from apps.vacancy_request.services import VacancyRequestService

User = get_user_model()


class VacancyRequestTestCase(TestCase):
    def setUp(self):
        self.department_lead = User.objects.create(username="Department Lead")
        self.hr_admin = User.objects.create(username="HR Admin")
        self.vacancy_request = VacancyRequest.objects.create(
            requester=self.department_lead,
            title='Python backend developer',
            department=Department.IT,
            city=City.BISHKEK,
            requirements='''Базовые знания Python''',
            responsibilities='''Писать код на Python''',
            min_salary=20000,
            max_salary=100000,
        )

    def test_set_vacancy_request_attribs(self):
        test_instance = VacancyRequestService.set_vacancy_request_attribs(
            self.vacancy_request,
            status=VacancyRequestStatus.APPROVED,
            approved_at=timezone.now(),
            approver=self.hr_admin,
        )
        self.assertEqual(test_instance, self.vacancy_request)
        self.assertEqual(test_instance.status, VacancyRequestStatus.APPROVED)
        self.assertEqual(test_instance.approver, self.hr_admin)
        self.assertEqual(test_instance.requester, self.department_lead)
        self.assertEqual(test_instance.department, Department.IT)
        self.assertEqual(test_instance.city, City.BISHKEK)

    def test_approve_vacancy_request(self):
        test_instance = VacancyRequestService.approve(self.vacancy_request, self.hr_admin)
        self.assertEqual(test_instance, self.vacancy_request)
        self.assertEqual(test_instance.status, VacancyRequestStatus.APPROVED)
        self.assertEqual(test_instance.approver, self.hr_admin)

    def test_reject_vacancy_request(self):
        test_instance = VacancyRequestService.reject(self.vacancy_request, self.hr_admin, 'Просто так')
        self.assertEqual(test_instance, self.vacancy_request)
        self.assertEqual(test_instance.status, VacancyRequestStatus.REJECTED)
        self.assertEqual(test_instance.approved_at, None)
        self.assertEqual(test_instance.approver, self.hr_admin)
        self.assertEqual(test_instance.rejected_reason, 'Просто так')

    def test_send_for_revision(self):
        test_instance = VacancyRequestService.send_for_revision(self.vacancy_request)
        self.assertEqual(test_instance, self.vacancy_request)
        self.assertEqual(test_instance.approved_at, None)
        self.assertEqual(test_instance.approver, None)
        self.assertEqual(test_instance.status, VacancyRequestStatus.NEEDS_REVISION)

    def test_resubmit(self):
        test_instance = VacancyRequestService.resubmit(self.vacancy_request)
        self.assertEqual(test_instance, self.vacancy_request)
        self.assertEqual(test_instance.approved_at, None)
        self.assertEqual(test_instance.approver, None)
        self.assertEqual(test_instance.status, VacancyRequestStatus.IN_REVIEW)