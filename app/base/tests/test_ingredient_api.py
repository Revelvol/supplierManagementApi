from django.test import TestCase
from base.models import Ingredient, Function, Unit
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


def create_function():
    name = 'Emulsifier'
    function = Function.objects.create(name=name)
    return function


def create_unit():
    name = 'grams'
    abbreviation = 'gr'
    conversion_rate = 1000.00
    unit = Unit.objects.create(name=name, abbreviation=abbreviation, conversion_rate=conversion_rate)
    return unit


def create_ingredient():
    name = 'IngredientA Washed up 500'
    quantity = 1.00
    price = 10.20
    is_used = True
    unit = create_unit()
    function = create_function()

    ingredient = Ingredient.objects.create(name=name,
                                           quantity=quantity,
                                           price=price,
                                           function=function,
                                           unit=unit,
                                           is_used=is_used)
    return ingredient


INGREDIENT_URL = reverse('ingredient:ingredient-list')


def detail_ingredient_url(ingredient_id):
    """Create and return a tag detail url."""
    return reverse('ingredient:ingredient-detail', args=[ingredient_id])


class PublicTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_public_ingredient_access_unauthorized(self):
        payload = {
            'name': 'hello',
            'quantity': 2.00,
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
        create_function()
        payload = {
            'name': 'hello',
            'quantity': 2.0,
            'price': 10.30,
            'is_used': True,
            'function': {
                'name': 'Emulsifier Food'
            },
            'unit': {
                'name': 'grams',
                'abbreviation': 'gr',
                'conversion_rate': 1
            },
        }
        res = self.client.post(INGREDIENT_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        ingredient = res.data
        for key, value in payload.items():
            if key != 'price ' or key != 'quantity':
                continue
            self.assertEqual(ingredient[key], value)

    def test_create_ingredient_fail_no_name_and_no_unit(self):
        payload = {
            'quantity': 2.00,
            'price': 10.30,
            'is_used': True
        }
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_function_inside_ingredient_with_same_name(self):
        create_unit()
        create_function()
        payload = {
            'name': 'hello',
            'quantity': 2.0,
            'price': 10.30,
            'is_used': True,
            'function': {
                'name': 'Emulsifier'
            },
            'unit': {
                'name': 'grams',
                'abbreviation': 'gr',
                'conversion_rate': 1
            },
        }

        res = self.client.post(INGREDIENT_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(1, Unit.objects.all().count())
        self.assertEqual(1, Function.objects.all().count())

    def test_update_function_without_function_and_unit(self):
        payload = {
            'name': 'hello',
            'quantity': 2.0,
            'function': {
                'name': 'Surfactant'
            },
            'unit': {
                'name': 'grams',
                'abbreviation': 'gr',
                'conversion_rate': 1
            },
        }
        ingredient = create_ingredient()
        detail_url = detail_ingredient_url(ingredient.id)
        res = self.client.patch(detail_url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(1, Unit.objects.all().count())
        self.assertEqual(2, Function.objects.all().count())


