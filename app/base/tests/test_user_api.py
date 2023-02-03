from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.contrib.auth.models import Group
from rest_framework.test import APIClient
from rest_framework import status
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


CREATE_USER_URL = reverse('user:create')
CREATE_TOKEN_URL = reverse('user:token')


class PublicTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'name': 'juliusSutandi',
            'email': 'juliuse32q3123@gmail.com',
            'password': 'helloisitme',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn(payload['password'], res.data)

    def test_create_user_fail(self):
        payload = {
            'email': 'juliussutandi@gmail.com',
            'password': 'hell',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(get_user_model().objects.all().count(), 1)

    def test_create_token_success(self):
        create_user()
        payload = {
            'email': 'juliussutandi@gmail.com',
            'password': 'testing1sada1',
        }
        res = self.client.post(CREATE_TOKEN_URL, payload)
        self.assertEqual(res.status_code, 200)
        self.assertIn('token', res.data)

    def test_create_token_fail(self):
        create_user()
        payload = {
            'email': 'julius@gmail.com',
            'password': 'testing1a1',
        }
        res = self.client.post(CREATE_TOKEN_URL, payload)
        self.assertEqual(res.status_code, 400)


#ME_URL = reverse('user:me')
class PrivateTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()
