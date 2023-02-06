from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from base.models import Unit


UNIT_URL = reverse('ingredient:unit-list')


def detail_unit_url(unit_id):
    """Create and return a tag detail url."""
    return reverse('ingredient:function-detail', args=[unit_id])


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
    name = 'grams'
    abbreviation = 'gr'
    conversion_rate = 1000.00
    unit = Unit.objects.create(name=name, abbrevation=abbreviation, conversion_rate=conversion_rate)
    return unit



class PublicTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_public_ingredient_access_unauthorized(self):
        payload = {
            'name': 'inch',
            'abbreviation':'inc',
            'conversion_rate' : 1002.23,
        }
        res = self.client.post(UNIT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_create_ingredient_successful(self):
        payload = {
            'name': 'inch',
            'abbreviation': 'inc',
            'conversion_rate': 1002.23,
        }
        res = self.client.post(UNIT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        function = res.data
        for key, value in payload.items():
            if key == 'conversion_rate':
                continue
            self.assertEqual(function[key], value)
