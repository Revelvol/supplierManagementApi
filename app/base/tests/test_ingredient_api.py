from django.test import TestCase
from base.models import Ingredient
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
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


def create_ingredient():
    name = 'IngredientA Washed up 500'
    quantity = 1.00
    price = 10.20
    is_used = True

    ingredient = Ingredient.objects.create(name=name,
                                           quantity=quantity,
                                           price=price,
                                           is_used=is_used)
    return ingredient


INGREDIENT_URL = reverse('ingredient:ingredient-list')


class PublicTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_public_ingredient_access_unauthorized(self):
        payload = {
            'name': 'hello',
            'quantity' : 2.00,
            'price': 10.30,
            'is_used': True
        }
        res = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_create_ingredient_successful(self):
        payload = {
            'name': 'hello',
            'quantity': 2.0,
            'price': 10.30,
            'is_used': True
        }
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        ingredient = res.data
        for key, value in payload.items():
            if key != 'price ' or key != 'quantity':
                continue
            self.assertEqual(ingredient[key], value)

    def test_create_ingredient_fail_no_name(self):
        payload = {
            'quantity': 2.00,
            'price': 10.30,
            'is_used': True
        }
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


