from django.test import TestCase
from base.models import Ingredient
from django.contrib.auth import get_user_model


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


class PublicTestApi(TestCase):
    pass

class PrivateTestApi(TestCase):
    pass
