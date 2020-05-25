from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from core.models import Component
from info.serializers import ComponentSerializer

COMPONENTS_URL = reverse('info:component-list')


class PublicComponentsApiTest(TestCase):
    """test publicly available component api tests"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """401 if unauthorized access"""
        res = self.client.get(COMPONENTS_URL)
        self.assertEqual(res.status_code, 401)


class PrivateComponentsApiTest(TestCase):
    """test private api tests"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="test123")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieving_components(self):
        """test tags retrieved correctly"""
        Component.objects.create(user=self.user, name="login")
        Component.objects.create(user=self.user, name="logout")
        res = self.client.get(COMPONENTS_URL)
        components = Component.objects.all().order_by("-name")
        serializer = ComponentSerializer(components, many=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_components_limited_to_user(self):
        """test returerned only related to user"""
        user2 = get_user_model().objects.create_user(
            email="other@test.com", password="test123")
        Component.objects.create(user=user2, name="login")
        component = Component.objects.create(user=self.user, name="logout")
        res = self.client.get(COMPONENTS_URL)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], component.name)

    def test_create_component_successful(self):
        """test creating new component"""
        payload = {'name': 'chart'}
        self.client.post(COMPONENTS_URL, payload)

        exists = Component.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """test creating tag with invalid payload"""
        payload = {"name": ""}
        res = self.client.post(COMPONENTS_URL, payload)
        self.assertEqual(res.status_code, 400)
