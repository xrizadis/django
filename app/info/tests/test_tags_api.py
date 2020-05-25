from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from core.models import Tag
from info.serializers import TagSerializer

TAGS_URL = reverse('info:tag-list')


class PublicTagsApiTest(TestCase):
    """test public api tests"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """401 if unauthorized access"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, 401)


class PrivateTagsApiTest(TestCase):
    """test private api tests"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="test123")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieving_tags(self):
        """test tags retrieved correctly"""
        Tag.objects.create(user=self.user, name="javascript")
        Tag.objects.create(user=self.user, name="python")
        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """test returerned only related to user"""
        user2 = get_user_model().objects.create_user(
            email="other@test.com", password="test123")
        Tag.objects.create(user=user2, name="c++")
        tag = Tag.objects.create(user=self.user, name="javascript")
        res = self.client.get(TAGS_URL)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tags_successful(self):
        """test creating new tag"""
        payload = {'name': 'test tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """test creating tag with invalid payload"""
        payload = {"name": ""}
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, 400)
