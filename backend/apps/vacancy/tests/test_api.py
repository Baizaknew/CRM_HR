from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.utils import timezone

from apps.user.tests.factories import HrLeadFactory, DepartmentHeadFactory, RecruiterFactory
from apps.vacancy.choices import Priority
from apps.vacancy.models import Vacancy
from apps.vacancy.tests.factories import VacancyStatusFactory, VacancyFactory

class VacancyAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hr_user = HrLeadFactory()
        cls.dh_user_1 = DepartmentHeadFactory()
        cls.dh_user_2 = DepartmentHeadFactory()
        cls.recruiter_1 = RecruiterFactory()
        cls.recruiter_2 = RecruiterFactory()

        cls.status_review_in_dh = VacancyStatusFactory(name="На рассмотрении у руководителя", is_default=True)
        cls.status_opened = VacancyStatusFactory(name="Открыта", is_opened=True)
        cls.status_closed = VacancyStatusFactory(name="Закрыта", is_closed=True)
        cls.status_on_hold = VacancyStatusFactory(name="Ожидание")

        cls.vac_dh1_rec1_opened = VacancyFactory(
            department_lead=cls.dh_user_1,
            recruiter=cls.recruiter_1,
            status=cls.status_opened,
            opened_at=timezone.now()
        )
        cls.vac_dh2_rec2_opened = VacancyFactory(
            department_lead=cls.dh_user_2,
            recruiter=cls.recruiter_2,
            status=cls.status_opened,
            opened_at=timezone.now()
        )
        cls.vac_dh1_new = VacancyFactory(
            department_lead=cls.dh_user_1,
            recruiter=None,
            status=cls.status_review_in_dh,
            opened_at=None
        )
        cls.vac_dh1_rec1_closed = VacancyFactory(
            department_lead=cls.dh_user_1,
            recruiter=cls.recruiter_1,
            status=cls.status_closed,
            opened_at=timezone.now() - timezone.timedelta(days=5),
            closed_at=timezone.now()
        )

        cls.list_url = reverse('vacancy-list')
        cls.detail_url = lambda pk: reverse('vacancy-detail', kwargs={'pk': pk})

    def test_list_permissions(self):
        test_cases = [
            (None, status.HTTP_401_UNAUTHORIZED, 0),
            (self.hr_user, status.HTTP_200_OK, 4),
            (self.dh_user_1, status.HTTP_200_OK, 3),
            (self.recruiter_1, status.HTTP_200_OK, 2),
            (self.dh_user_2, status.HTTP_200_OK, 1),
            (self.recruiter_2, status.HTTP_200_OK, 1),
        ]
        for user, expected_status, expected_count in test_cases:
            with self.subTest(user=user.username if user else "Anonymous"):
                self.client.force_authenticate(user=user)
                response = self.client.get(self.list_url)
                self.assertEqual(response.status_code, expected_status)
                if expected_status == status.HTTP_200_OK:
                    results = response.data if isinstance(response.data, list) else response.data.get('results', [])
                    self.assertEqual(len(results), expected_count)

    def test_retrieve_permissions(self):
        accessible_cases = [
            (self.hr_user, self.vac_dh1_rec1_opened.pk),
            (self.dh_user_1, self.vac_dh1_rec1_opened.pk),
            (self.recruiter_1, self.vac_dh1_rec1_opened.pk),
        ]
        inaccessible_cases = [
            (None, self.vac_dh1_rec1_opened.pk, status.HTTP_401_UNAUTHORIZED),
            (self.dh_user_2, self.vac_dh1_rec1_opened.pk, status.HTTP_404_NOT_FOUND),
            (self.recruiter_2, self.vac_dh1_rec1_opened.pk, status.HTTP_404_NOT_FOUND),
        ]

        for user, pk in accessible_cases:
             with self.subTest(user=user.username, access="allowed"):
                self.client.force_authenticate(user=user)
                url = self.detail_url(pk)
                response = self.client.get(url)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data['id'], pk)

        for user, pk, expected_status in inaccessible_cases:
             with self.subTest(user=user.username if user else "Anonymous", access="denied"):
                self.client.force_authenticate(user=user)
                url = self.detail_url(pk)
                response = self.client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_update_permissions_denied_for_dh(self):
        self.client.force_authenticate(user=self.dh_user_1)
        url = self.detail_url(self.vac_dh1_rec1_opened.pk)
        data = {"priority": Priority.HIGH}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_by_hr_can_change_recruiter_and_status(self):
        self.client.force_authenticate(user=self.hr_user)
        url = self.detail_url(self.vac_dh1_rec1_opened.pk)
        data = {
            "recruiter": self.recruiter_2.pk,
            "status": self.status_on_hold.pk
        }
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.vac_dh1_rec1_opened.refresh_from_db()
        self.assertEqual(self.vac_dh1_rec1_opened.recruiter, self.recruiter_2)
        self.assertEqual(self.vac_dh1_rec1_opened.status, self.status_on_hold)

    def test_update_by_recruiter_can_change_status(self):
        self.client.force_authenticate(user=self.recruiter_1)
        url = self.detail_url(self.vac_dh1_rec1_opened.pk)
        data = {
            "status": self.status_on_hold.pk
        }
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.vac_dh1_rec1_opened.refresh_from_db()
        self.assertEqual(self.vac_dh1_rec1_opened.status, self.status_on_hold)

    def test_update_by_recruiter_cannot_change_priority(self):
        self.client.force_authenticate(user=self.recruiter_1)
        url = self.detail_url(self.vac_dh1_rec1_opened.pk)
        initial_priority = self.vac_dh1_rec1_opened.priority
        data = {
            "priority": Priority.HIGH,
            "status": self.status_on_hold.pk
        }
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vac_dh1_rec1_opened.refresh_from_db()
        self.assertEqual(self.vac_dh1_rec1_opened.status, self.status_on_hold)
        self.assertEqual(self.vac_dh1_rec1_opened.priority, initial_priority)

    def test_update_by_other_recruiter_denied(self):
        self.client.force_authenticate(user=self.recruiter_2)
        url = self.detail_url(self.vac_dh1_rec1_opened.pk)
        data = {"status": self.status_on_hold.pk}
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) # FIXED or 404?

    def test_perform_update_set_opened_at_on_status_change(self):
        self.client.force_authenticate(user=self.hr_user)
        url = self.detail_url(self.vac_dh1_new.pk)
        self.assertIsNone(self.vac_dh1_new.opened_at)
        data = {"status": self.status_opened.pk}

        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.vac_dh1_new.refresh_from_db()
        self.assertIsNotNone(self.vac_dh1_new.opened_at)
        self.assertAlmostEqual(self.vac_dh1_new.opened_at, timezone.now(), delta=timezone.timedelta(seconds=2))

    def test_perform_update_set_closed_at_on_status_change(self):
        self.client.force_authenticate(user=self.hr_user)
        url = self.detail_url(self.vac_dh1_rec1_opened.pk)
        self.assertIsNone(self.vac_dh1_rec1_opened.closed_at)
        data = {"status": self.status_closed.pk}

        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.vac_dh1_rec1_opened.refresh_from_db()
        self.assertIsNotNone(self.vac_dh1_rec1_opened.closed_at)
        self.assertAlmostEqual(self.vac_dh1_rec1_opened.closed_at, timezone.now(), delta=timezone.timedelta(seconds=2))

    def test_destroy_permissions(self):
        users_denied = [self.dh_user_1, self.recruiter_1]
        pk_to_delete = self.vac_dh1_new.pk

        for user in users_denied:
            with self.subTest(user=user.username, access="denied"):
                self.client.force_authenticate(user=user)
                url = self.detail_url(pk_to_delete)
                response = self.client.delete(url)
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                self.assertTrue(Vacancy.objects.filter(pk=pk_to_delete).exists())

        with self.subTest(user=self.hr_user.username, access="allowed"):
            initial_count = Vacancy.objects.count()
            self.client.force_authenticate(user=self.hr_user)
            url = self.detail_url(pk_to_delete)
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(Vacancy.objects.count(), initial_count - 1)
            self.assertFalse(Vacancy.objects.filter(pk=pk_to_delete).exists())