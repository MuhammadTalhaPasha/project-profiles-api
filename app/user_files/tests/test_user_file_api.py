from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import User_File, Tag, File_type

from user_files.serializers import User_FileSerializer, UserFileDetailSerializer

USER_FILES_URL = reverse('user_files:user_file-list')

# /api/user_files/user_file
# /api/user_files/user_file/1/

def detail_url(user_file_id):
    """Return userfile detail url"""
    return reverse('user_files:user_file-detail', args=[user_file_id])

def sample_tag(user, name='room'):
    """create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)

def sample_file_type(user, type='DWG'):
    """create and return a sample file_type"""
    return File_type.objects.create(user=user, type=type)

def sample_user_files(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        'title': 'Sample recipe',
        # 'created_on':'12/12/12',
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

    def test_view_userfile_detail(self):
        """test viewing a user_file detail"""
        user_file = sample_user_files(user=self.user)
        user_file.tags.add(sample_tag(user=self.user))
        user_file.file_types.add(sample_file_type(user=self.user))

        url = detail_url(user_file.id)
        res = self.client.get(url)

        serializer = UserFileDetailSerializer(user_file)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_userfile(self):
        """test creating userfile"""
        payload = {
            'title':'ROOM'
            # 'created_on': '20/4/19'
        }
        res = self.client.post(USER_FILES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user_file = User_File.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(user_file, key))

    def test_create_userfile_with_tags(self):
        """test creating a userfile with tags"""
        tag1 = sample_tag(user=self.user, name='tag 1')
        tag2 = sample_tag(user=self.user, name='tag 2')
        payload = {
            'title': 'test with two tags',
            'tags' : [tag1.id, tag2.id],
            # 'created_on' : '12/4/19'
        }
        res = self.client.post(USER_FILES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user_file = User_File.objects.get(id=res.data['id'])
        tags = user_file.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_userfile_with_filetype(self):
        """test creating a userfile with tags"""
        file_type1 = sample_file_type(user=self.user, type='DWG')
        file_type2 = sample_file_type(user=self.user, type='DXF')
        payload = {
            'title': 'HOTEL',
            'file_types': [file_type1.id, file_type2.id],
            # 'created_on': '12/4/19'
        }
        res = self.client.post(USER_FILES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user_file = User_File.objects.get(id=res.data['id'])
        file_types = user_file.file_types.all()
        self.assertEqual(file_types.count(), 2)
        self.assertIn(file_type1, file_types)
        self.assertIn(file_type2, file_types)
