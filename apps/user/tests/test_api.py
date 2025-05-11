from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.user.tests.factories import HrLeadFactory, RecruiterFactory, DepartmentHeadFactory


class UserTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hr_user = HrLeadFactory()
        cls.recruiter_1 = RecruiterFactory()
        cls.recruiter_2 = RecruiterFactory()
        cls.dh_user = DepartmentHeadFactory()

        # urls
        cls.list_url = reverse('users-list')
        cls.detail_url = lambda pk: reverse('users-detail', kwargs={'pk': pk})

    def test_error_create(self):
        test_cases = (
            (self.recruiter_1, status.HTTP_403_FORBIDDEN,),
            (self.recruiter_2, status.HTTP_403_FORBIDDEN,),
            (self.dh_user, status.HTTP_403_FORBIDDEN,)
        )
        for user, expected_status in test_cases:
            with self.subTest(user=user.username):
                self.client.force_authenticate(user=user)
                data = {
                    'username': 'test',
                    'first_name': 'test',
                    'last_name': 'test',
                    'email': 'test@gmail.com',
                    'role': 'RECRUITER',
                    'password': 'Bastard123',
                }
                response = self.client.post(self.list_url, data=data)
                self.assertEqual(response.status_code, expected_status)

    def test_success_create(self):
        self.client.force_authenticate(self.hr_user)
        data = {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@gmail.com',
            'role': 'RECRUITER',
            'password': 'Bastard123',
        }

        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_success_users_list(self):
        self.client.force_authenticate(self.hr_user)
        response = self.client.get(self.list_url)

        self.assertEqual(len(response.data), 4)

    def test_success_update(self):
        self.client.force_authenticate(self.recruiter_1)
        url = self.detail_url(self.recruiter_1.pk)

        data = {
            'username': 'test_username',
        }

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.recruiter_1.refresh_from_db()
        self.assertEqual(self.recruiter_1.username, data.get('username'))

    def test_error_update(self):
        self.client.force_authenticate(self.recruiter_2)
        url = self.detail_url(self.recruiter_1.pk)

        data = {
            'username': 'test_username',
        }

        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
