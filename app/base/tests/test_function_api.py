from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from base.models import Function


FUNCTION_URL = reverse('ingredient:function-list')


def detail_function_url(function_id):
    """Create and return a tag detail url."""
    return reverse('ingredient:function-detail', args=[function_id])


def create_user():
    user = get_user_model().objects.create_user(name='julius',
                                                email='juliussutandi@gmail.com',
                                                password='testing1sada1', )
    return user


def create_super_user():
    user = get_user_model().objects.create_superuser(name='julius',
                                                     email='juliussutandi1@gmail.com',
                                                     password='testing1sada1', )
    return user


def create_function():
    name = 'Emulsifier Food'
    function = Function.objects.create(name=name)
    return function



class PublicTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_public_ingredient_access_unauthorized(self):
        payload = {
            'name': 'Emulsifier Food',
        }
        res = self.client.post(FUNCTION_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_create_ingredient_successful(self):
        payload = {
            'name': 'Emulsifier Food2',
        }
        res = self.client.post(FUNCTION_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        function = res.data
        for key, value in payload.items():
            self.assertEqual(function[key], value)
