from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import File_type

from user_files.serializers import File_typeSerializer

FILE_TYPE_URL = reverse('user_files:file_type-list')

class PublicFileTypeApiTests(TestCase):
    """test the publicily available file_type api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required to access the endpoint"""

        res = self.client.get(FILE_TYPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateFileTypeApiTests(TestCase):
    """tests private file_type can be retrived by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@pashadev.com',
            'test123'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_file_type_list(self):
        """test retriving a list of file_type"""
        File_type.objects.create(user=self.user, type='DWG')
        File_type.objects.create(user=self.user, type='DEG')

        res = self.client.get(FILE_TYPE_URL)

        file_type = File_type.objects.all().order_by('-type')
        serializer = File_typeSerializer(file_type, many = True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_file_type_limited_to_user(self):
        """test that the file_type for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'test2@pashadev.com',
            'testpass'
        )
        File_type.objects.create(user=user2, type='DXF')

        file_type = File_type.objects.create(user=self.user, type='DWG')

        res = self.client.get(FILE_TYPE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['type'], file_type.type)

    def test_create_file_type_successful(self):
        """test create a new type"""
        payload = {'type': 'DXF'}
        self.client.post(FILE_TYPE_URL, payload)

        exists = File_type.objects.filter(
            user=self.user,
            type=payload['type'],
        ).exists()
        self.assertTrue(exists)

    def test_create_type_file_invalid(self):
        """test creating invalid file type fails"""
        payload = {'type': ''}
        res = self.client.post(FILE_TYPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
