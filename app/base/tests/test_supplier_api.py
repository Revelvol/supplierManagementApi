from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from base.models import Supplier

SUPPLIER_URL = reverse('ingredient:supplier-list')


def detail_supplier_url(supplier_id):
    """Create and return a tag detail url."""
    return reverse('ingredient:supplier-detail', args=[supplier_id])


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


def create_supplier():
    name = 'pT. Supplier A'
    location = 'Indonesia, Jakarta'
    phone = '+62866094'
    supplier = Supplier.objects.create(name=name, location=location, phone=phone)
    return supplier


class PublicTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_public_ingredient_access_unauthorized(self):
        payload = {
            'name': 'supplier2',
            'location': 'asdajsdasdasd',
            'phone': '+62832154730812430',
        }
        res = self.client.post(SUPPLIER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_create_ingredient_successful(self):
        payload = {
            'name': 'supplier3',
            'location': 'asdajsdasdasd1233123',
            'phone': '+6283215473081',
        }
        res = self.client.post(SUPPLIER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        function = res.data
        for key, value in payload.items():
            self.assertEqual(function[key], value)
