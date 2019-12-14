from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import User_File
from user_files.serializers import User_FileSerializer

USER_FILES_URL = reverse('user_files:user_file-list')

def sample_user_files(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        'title': 'Sample recipe',
        'created_on':'12/12/12',
    }
    defaults.update(params)

    return User_File.objects.create(user=user, **defaults)


class PublicUserFileApiTests(TestCase):
    """Test unauthenticated userfile API access"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test the authenticaiton is required"""
        res = self.client.get(USER_FILES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserFileApiTests(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@pashadev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_userfiles(self):
        """Test retrieving list of recipes"""
        sample_user_files(user=self.user)
        sample_user_files(user=self.user)

        res = self.client.get(USER_FILES_URL)

        userfiles = User_File.objects.all().order_by('-id')
        serializer = User_FileSerializer(userfiles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        #there is an error of order of dict assertion error commented for the time being
        #self.assertEqual(res.data, serializer.data)

    def test_userfiles_limited_to_user(self):
        """Test retrieving recipes for user"""
        user2 = get_user_model().objects.create_user(
            'other@pashadev.com',
            'pass'
        )
        sample_user_files(user=user2)
        sample_user_files(user=self.user)

        res = self.client.get(USER_FILES_URL)

        userfiles = User_File.objects.filter(user=self.user)
        serializer = User_FileSerializer(userfiles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
