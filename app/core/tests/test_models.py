from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email="test@test.com", password="test122"):
    """create a sampe user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """test create a new user with email and password"""
        email = "test@test.com"
        password = "test"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        """test the email for the new user is normalised"""
        email = "test@TEST.COM"
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test no email raises error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_suer_upser(self):
        """Test create a new super user """
        user = get_user_model().objects.create_superuser(
            email="test@test.com",
            password="test123"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """test tag representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="java"
        )
        self.assertEqual(str(tag), tag.name)

    def test_components_str(self):
        """test the component string representation"""
        component = models.Component.objects.create(
            user=sample_user(),
            name="login"
        )
        self.assertEqual(str(component), component.name)
