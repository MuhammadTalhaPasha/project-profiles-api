from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@pashadev.com', password='test123'):
    """create a sample_user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        """test creating a new user with email is test_create_user_with_email_successfull"""
        email = 'test@pashadev.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    def test_new_user_email_normalized(self):
	    """Test the email for a new user is normalized"""
	    email = 'test@PASHADEV.com'
	    user = get_user_model().objects.create_user(email, 'test123')

	    self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test createing uesr with no email raises"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'test123')

    def test_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
        'test@londonappdev.com',
        'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_file_type_str(self):
        """test the file_type string representation"""
        file_type = models.File_type.objects.create(
            user = sample_user(),
            type = 'DXF'
        )

        self.assertEqual(str(file_type), file_type.type)

    def test_uesr_files_str(self):
        """tests the user_files string representation"""
        user_files = models.User_Files.objects.create(
            user = sample_user(),
            title='file room',
            created_on='23/5/19'
        )

        self.assertEqual(str(user_files), user_files.title)
