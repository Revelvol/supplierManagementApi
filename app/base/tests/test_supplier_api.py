from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from base.models import Supplier, Pic, Ingredient, Unit, Function

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
    phone = '+628660942'
    supplier = Supplier.objects.create(name=name, location=location, phone=phone)
    return supplier


class PublicTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_public_supplier_access_unauthorized(self):
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

    def test_create_supplier_successful(self):
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

    def test_create_supplier_with_multiple_pic(self):
        payload = {
            'name': 'test supplier',
            'location': 'test location',
            'phone': '+6283215473081',
            'pic': [
                {'name': 'test person1',
                 'position': 'test position',
                 'email': 'testperson2@example.com',
                 }, {
                    'name': 'test person2',
                    'position': 'test position',
                    'email': 'testperson2@example.com',
                }
            ]
        }
        res = self.client.post(SUPPLIER_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(2, Pic.objects.all().count())
        function = res.data
        for key, value in payload.items():
            if key == 'pic':
                continue
            self.assertEqual(function[key], value)

    def test_create_supplier_with_multiple_same_pic(self):
        payload = {
            'name': 'test supplier',
            'location': 'test location',
            'phone': '+6283215473081',
            'pic': [
                {'name': 'test person1',
                 'position': 'test position',
                 'email': 'testperson2@example.com',
                 }, {
                    'name': 'test person1',
                    'position': 'test position',
                    'email': 'testperson1@example.com',
                }
            ]
        }
        res = self.client.post(SUPPLIER_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(2, Pic.objects.all().count())
        function = res.data
        for key, value in payload.items():
            if key == 'pic':
                continue
            self.assertEqual(function[key], value)

    def test_create_supplier_with_multiple_same_pic_and_ingredient(self):
        payload = {
            'name': 'test supplier',
            'location': 'test location',
            'phone': '+6283215473081',
            'pic': [
                {
                    'name': 'test person1',
                    'position': 'test position',
                    'email': 'testperson2@example.com',
                },
                {
                    'name': 'test person1',
                    'position': 'test position',
                    'email': 'testperson1@example.com',
                }
            ],
            'ingredient': [
                {
                    'name': 'ceban',
                    'price': 10023.2,
                    'quantity': 123421,
                    'function':
                        {
                            'name': 'money'
                        },

                    'unit':
                        {
                            'name' : 'Ton',
                            'abbreviation': 'tn',
                            'conversion_rate': 1000,
                        },

                }
            ]
        }
        res = self.client.post(SUPPLIER_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(2, Pic.objects.all().count())
        self.assertEqual(1, Ingredient.objects.all().count())
        self.assertEqual(1, Unit.objects.all().count())
        self.assertEqual(1, Function.objects.all().count())

        function = res.data
        for key, value in payload.items():
            if key == 'pic' or key == 'ingredient':
                continue
            self.assertEqual(function[key], value)

    def test_update_supplier_successful(self):

        supplier = create_supplier()
        detail_url = detail_supplier_url(supplier_id=supplier.id)
        payload = {
            'name': 'supplier3',
            'location': 'asdajsdasdasd1233123',
        }

        res = self.client.patch(detail_url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for key, value in payload.items():
            if key == 'pic':
                continue
            self.assertEqual(res.data[key], value)
        self.assertEqual(1, Supplier.objects.all().count())

    def test_update_supploer_with_pic_fail(self):

        supplier = create_supplier()
        detail_url = detail_supplier_url(supplier_id=supplier.id)
        payload = {
            'name': 'supplier3',
            'location': 'asdajsdasdasd1233123',
            'pic': [
                {'name': 'test person1',
                 'position': 'test position',
                 'email': 'testperson2@example.com',
                 }, {
                    'name': 'test person1',
                    'position': 'test position',
                    'email': 'testperson1@example.com',
                }
            ]

        }

        res = self.client.patch(detail_url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(0, Pic.objects.all().count())

    def test_update_supploer_with_pic_fail_and_ingredient_fail(self):

        supplier = create_supplier()
        detail_url = detail_supplier_url(supplier_id=supplier.id)
        payload = {
            'name': 'supplier3',
            'location': 'asdajsdasdasd1233123',
            'pic': [
                {'name': 'test person1',
                 'position': 'test position',
                 'email': 'testperson2@example.com',
                 }, {
                    'name': 'test person1',
                    'position': 'test position',
                    'email': 'testperson1@example.com',
                }
            ],
            'ingredient': [
                {
                    'name': 'ceban',
                    'price': 10023.2,
                    'quantity': 123421,
                    'function':
                        {
                            'name': 'money'
                        },

                    'unit':
                        {
                            'name': 'Ton',
                            'abbreviation': 'tn',
                            'conversion_rate': 1000,
                        },

                }
            ]

        }

        res = self.client.patch(detail_url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(0, Pic.objects.all().count())
        self.assertEqual(0, Ingredient.objects.all().count())

    def test_update_supplier_with_pic_data_not_complete(self):

        supplier = create_supplier()
        detail_url = detail_supplier_url(supplier_id=supplier.id)
        payload = {
            'name': 'supplier3',
            'location': 'asdajsdasdasd1233123',
            'pic': [
                {'name': 'test person1',
                 'position': 'test position',
                 'email': 'testperson2@example.com',
                 },
                {
                    'email': 'test@gmail.com',
                }
            ],
        }

        res = self.client.patch(detail_url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(0, Pic.objects.all().count())

