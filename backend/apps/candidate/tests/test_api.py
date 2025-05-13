from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from apps.candidate.tests.factories import CandidateTagFactory
from apps.user.tests.factories import HrLeadFactory, RecruiterFactory
from apps.vacancy_request.tests.factories import DepartmentHeadFactory

from django.urls import reverse


class CandidateTagAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # users
        cls.hr_lead = HrLeadFactory()
        cls.recruiter = RecruiterFactory()
        cls.dh_1 = DepartmentHeadFactory()
        cls.dh_2 = DepartmentHeadFactory()

        cls.tag = CandidateTagFactory()

        cls.list_url = reverse('candidate-application-tag-list')
        cls.detail_url = lambda pk: reverse('candidate-application-tag-detail', kwargs={'pk': pk})

    def test_success_list(self):
        self.client.force_authenticate(self.recruiter)
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 1)

    def test_error_create(self):
        self.client.force_authenticate(self.recruiter)
        data = {
            'name': 'test'
        }
        response = self.client.post(self.list_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_success_create(self):
        self.client.force_authenticate(self.hr_lead)
        data = {
            'title': 'test'
        }
        response = self.client.post(self.list_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_success_update(self):
        self.client.force_authenticate(self.hr_lead)
        url = self.detail_url(self.tag.pk)
        data = {
            'title': 'test2'
        }
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.tag.refresh_from_db()
        self.assertEqual(self.tag.title, data.get('title'))


    def test_error_update(self):
        self.client.force_authenticate(self.recruiter)
        url = self.detail_url(self.tag.pk)
        data = {
            'title': 'test2'
        }
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
