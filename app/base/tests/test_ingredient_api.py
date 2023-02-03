from django.test import TestCase
from base.models import Ingredient
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
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
    quantity = 1
    price = 10.20
    is_used = True

    ingredient = Ingredient.objects.create(name=name,
                                           quantity=quantity,
                                           price=price,
                                           is_used=is_used)
    return ingredient


INGREDIENT_URL = reverse('ingredient:ingredients')


class PublicTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_public_ingredient_access(self):
        pass


class PrivateTestApi(TestCase):
    def setUp(self):
        pass
