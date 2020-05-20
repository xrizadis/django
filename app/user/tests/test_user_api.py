from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the user api (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with a valid payload is successful"""
        payload = {
            'email': 'test5test@test.com',
            'password': 'testtesttest',
            'name': 'testname'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, 201)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test fail if email exists"""
        payload = {'email': 'test@test.com',
                   'password': 'testtesttest', 'name': 'test'}

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, 400)

    def test_password_too_short(self):
        """test password is more than 10 chars"""
        payload = {'email': 'test@test.com',
                   'password': 'test', 'name': 'test'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, 400)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """test that a token is created for thser user"""
        payload = {'email': 'test@test.com', 'password': 'test123'}

        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, 200)

    def test_create_token_invalid_credentials(self):
        """test that a token is not created if invalid credentials are given"""
        create_user(email="test@test.com", password="test123")
        payload = {"email": "test@test.com", "password": "testtesttest"}

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, 400)

    def test_create_token_no_user(self):
        """test that token is not created if user does not exist"""
        payload = {'email': 'test@test.com', 'password': 'test123'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, 400)

    def test_create_token_missing_field(self):
        """test email and password are required"""
        payload = {'email': 'test', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, 400)
