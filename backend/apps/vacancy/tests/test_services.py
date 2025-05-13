from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps.user.tests.factories import DepartmentHeadFactory, HrLeadFactory
from apps.vacancy.models import Vacancy
from apps.vacancy.services import VacancyService
from apps.vacancy.tests.factories import VacancyStatusFactory
from apps.vacancy_request.tests.factories import VacancyRequestFactory


class VacancyServiceTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.dh_user = DepartmentHeadFactory()
        cls.hr_user = HrLeadFactory()

        cls.default_vacancy_status = VacancyStatusFactory(name="На рассмотрении", is_default=True)
        cls.closed_status = VacancyStatusFactory(name="Закрыта", is_closed=True)

        cls.approved_request = VacancyRequestFactory(
            requester=cls.dh_user,
            status='APPROVED',
            approver=cls.hr_user,
            min_salary=50000,
            max_salary=100000
        )
        cls.request_no_salary = VacancyRequestFactory(
            requester=cls.dh_user,
            status='APPROVED',
            min_salary=None,
            max_salary=None
        )
        cls.request_only_max_salary = VacancyRequestFactory(
            requester=cls.dh_user,
            status='APPROVED',
            min_salary=None,
            max_salary=80000
        )

    def test_get_default_status_success(self):
        status = VacancyService.get_default_status()
        self.assertIsNotNone(status)
        self.assertEqual(status.pk, self.default_vacancy_status.pk)
        self.assertTrue(status.is_default)

    def test_get_default_status_raises_error_if_not_found(self):
        self.default_vacancy_status.is_default = False
        self.default_vacancy_status.save()

        with self.assertRaises(ValidationError) as cm:
            VacancyService.get_default_status()
        self.assertIn('Отсутствует дефолтный статус', str(cm.exception))

        self.default_vacancy_status.is_default = True
        self.default_vacancy_status.save()

    def test_create_vacancy_from_request_success(self):
        initial_vacancy_count = Vacancy.objects.count()

        created_vacancy = VacancyService.create(self.approved_request)

        self.assertIsNotNone(created_vacancy, "Метод create вернул None при успехе")
        self.assertIsInstance(created_vacancy, Vacancy)
        self.assertEqual(Vacancy.objects.count(), initial_vacancy_count + 1)

        self.assertEqual(created_vacancy.title, self.approved_request.title)
        self.assertEqual(created_vacancy.department, self.approved_request.department)
        self.assertEqual(created_vacancy.city, self.approved_request.city)
        self.assertEqual(created_vacancy.requirements, self.approved_request.requirements)
        self.assertEqual(created_vacancy.responsibilities, self.approved_request.responsibilities)
        self.assertEqual(created_vacancy.department_lead, self.approved_request.requester)
        self.assertEqual(created_vacancy.vacancy_request, self.approved_request)
        self.assertEqual(created_vacancy.status, self.default_vacancy_status)
        self.assertEqual(created_vacancy.salary, f"от {self.approved_request.min_salary} до {self.approved_request.max_salary}")
        self.assertIsNone(created_vacancy.recruiter)
        self.assertIsNone(created_vacancy.opened_at)
        self.assertIsNone(created_vacancy.closed_at)

    def test_create_vacancy_salary_formatting(self):
        vacancy_no_salary = VacancyService.create(self.request_no_salary)
        self.assertIsNotNone(vacancy_no_salary)
        self.assertIsNone(vacancy_no_salary.salary, "Поле salary должно быть None, если нет данных")

        vacancy_only_max = VacancyService.create(self.request_only_max_salary)
        self.assertIsNotNone(vacancy_only_max)
        self.assertEqual(vacancy_only_max.salary, f"от 0 до {self.request_only_max_salary.max_salary}")
