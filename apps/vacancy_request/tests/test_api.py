from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.user.tests.factories import HrLeadFactory, RecruiterFactory, DepartmentHeadFactory
from apps.vacancy.choices import Department, City
from apps.vacancy_request.choices import VacancyRequestStatus
from apps.vacancy_request.models import VacancyRequest
from apps.vacancy_request.tests.factories import VacancyRequestFactory

class VacancyRequestAPITests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # users
        cls.hr_lead = HrLeadFactory()
        cls.recruiter = RecruiterFactory()
        cls.dh_1 = DepartmentHeadFactory()
        cls.dh_2 = DepartmentHeadFactory()

        # vacancy_requests
        cls.req_dh1_in_review = VacancyRequestFactory(requester=cls.dh_1, status=VacancyRequestStatus.IN_REVIEW)
        cls.req_dh1_needs_revision = VacancyRequestFactory(requester=cls.dh_1, status=VacancyRequestStatus.NEEDS_REVISION)
        cls.req_dh1_approved = VacancyRequestFactory(requester=cls.dh_1, status=VacancyRequestStatus.APPROVED)
        cls.req_dh2_in_review = VacancyRequestFactory(requester=cls.dh_2, status=VacancyRequestStatus.IN_REVIEW)

        # urls
        cls.list_create_url = reverse('vacancy-request-list')

        cls.detail_url = lambda pk: reverse('vacancy-request-detail', kwargs={'pk': pk})
        cls.approve_url = lambda pk: reverse('vacancy-request-approve', kwargs={'pk': pk})
        cls.reject_url = lambda pk: reverse('vacancy-request-reject', kwargs={'pk': pk})
        cls.send_for_revision_url = lambda pk: reverse('vacancy-request-send-for-revision', kwargs={'pk': pk})
        cls.resubmit_url = lambda pk: reverse('vacancy-request-resubmit', kwargs={'pk': pk})

    def test_list_permissions_anonymous(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_permissions_recruiter(self):
        self.client.force_authenticate(self.recruiter)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_permissions_hr_lead(self):
        self.client.force_authenticate(self.hr_lead)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_list_filter_for_department_head(self):
        self.client.force_authenticate(self.dh_1)
        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        # Проверка на видимость своих и чужих заявок
        req_ids = {vac_request.get('id') for vac_request in response.data}

        self.assertIn(self.req_dh1_in_review.pk, req_ids)
        self.assertIn(self.req_dh1_approved.pk, req_ids)
        self.assertIn(self.req_dh1_needs_revision.pk, req_ids)
        self.assertNotIn(self.req_dh2_in_review.pk, req_ids)

    def test_create_permissions_hr_lead_or_recruiter(self):
        users_to_test = (self.hr_lead, self.recruiter)
        data = {
            'title': 'Тестовая заявка',
            'department': Department.QUALITY,
            'city': City.OSH,
            'requirements': 'Тестовые требования',
            'responsibilities': 'Тестовые обязанности',
        }
        for user in users_to_test:
            with self.subTest(user=user):
                self.client.force_authenticate(user)
                response = self.client.post(self.list_create_url, data=data)
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_success_by_department_head(self):
        self.client.force_authenticate(self.dh_1)
        initial_count = VacancyRequest.objects.count()
        data = {
            'title': 'Тестовая заявка',
            'department': Department.QUALITY,
            'city': City.OSH,
            'requirements': 'Тестовые требования',
            'responsibilities': 'Тестовые обязанности',
            'min_salary': 100000,
            'max_salary': 200000,
        }
        response = self.client.post(self.list_create_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])

        self.assertEqual(VacancyRequest.objects.count(), initial_count + 1)
        new_vacancy_request = VacancyRequest.objects.get(pk=response.data['id'])
        self.assertEqual(new_vacancy_request.status, VacancyRequestStatus.IN_REVIEW)
        self.assertEqual(new_vacancy_request.requester, self.dh_1)

    def test_approve_success_hr(self):
        self.client.force_authenticate(self.hr_lead)
        url = self.approve_url(self.req_dh1_in_review.pk)
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_approve_permissions_recruiter_and_department_head(self):
        users_to_test = (self.dh_1, self.recruiter)
        for user in users_to_test:
            with self.subTest(user=user):
                self.client.force_authenticate(user)
                url = self.approve_url(self.req_dh1_in_review.pk)
                response = self.client.post(url, data={})
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reject_success_hr(self):
        self.client.force_authenticate(self.hr_lead)
        url = self.reject_url(self.req_dh2_in_review.pk)
        data = {'rejected_reason': 'Просто так'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        vacancy_request = VacancyRequest.objects.get(pk=response.data['id'])
        self.assertEqual(vacancy_request.status, VacancyRequestStatus.REJECTED)

    def test_reject_permissions_recruiter_and_department_head(self):
        users_to_test = (self.dh_1, self.recruiter)
        for user in users_to_test:
            with self.subTest(user=user):
                self.client.force_authenticate(user)
                url = self.reject_url(self.req_dh2_in_review.pk)
                data = {'rejected_reason': 'Просто так'}
                response = self.client.post(url, data=data)
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reject_error(self):
        self.client.force_authenticate(self.hr_lead)
        url = self.reject_url(self.req_dh2_in_review.pk)
        data = {}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reject_permissions_hr(self):
        self.client.force_authenticate(self.hr_lead)
        url = self.reject_url(self.req_dh1_approved.pk)
        data = {'rejected_reason': 'Просто так'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_send_for_revision_success(self):
        self.client.force_authenticate(self.hr_lead)
        url = self.send_for_revision_url(self.req_dh2_in_review.pk)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_send_for_revision_error(self):
        self.client.force_authenticate(self.dh_1)  # Аутентифицируемся как Руководитель
        url = self.send_for_revision_url(self.req_dh2_in_review.pk)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_success_by_owner_in_needs_revision(self):
        self.client.force_authenticate(self.dh_1)
        url = self.detail_url(self.req_dh1_needs_revision.pk)
        data = {
            'title': 'Измененное название',
            'department': Department.IT,
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['department'], data['department'])

        # Проверка Базы данных
        self.req_dh1_in_review.refresh_from_db()
        self.assertEqual(self.req_dh1_needs_revision.title, data['title'])
        self.assertEqual(self.req_dh1_needs_revision.department, data['department'])
        self.assertEqual(self.req_dh1_needs_revision.status, VacancyRequestStatus.NEEDS_REVISION)

    def test_update_permissions_by_not_owner_in_needs_revision(self):
        self.client.force_authenticate(self.dh_2)
        url = self.detail_url(self.req_dh1_needs_revision.pk)
        data = {
            'title': 'Изменение с permissions'
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_inappropriate_status(self):
        self.client.force_authenticate(self.dh_1)
        url = self.detail_url(self.req_dh2_in_review.pk)
        data = {
            'title': 'Изменение не в подходящем статусе'
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_resubmit_success(self):
        self.client.force_authenticate(self.dh_1)
        url = self.resubmit_url(self.req_dh1_needs_revision.pk)
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка изменения в базе данных
        vacancy_request = VacancyRequest.objects.get(pk=response.data['id'])
        self.assertEqual(vacancy_request.status, VacancyRequestStatus.IN_REVIEW)

    def test_resubmit_error(self):
        self.client.force_authenticate(self.dh_1)
        url = self.resubmit_url(self.req_dh1_in_review.pk)
        data = {}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
