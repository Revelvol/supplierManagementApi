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
ME_URL = reverse('user:me')


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

    def test_retrieve_me_fail(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_me_success(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    def test_patch_me_sucess(self):

        payload = {
            'name': 'kentel',
            'password': '1231243141353523'
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(self.user.name, payload['name'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_put_me_sucess(self):
        payload = {
            'name': 'kentel',
            'email': 'juliu@gmail.com',
            'password': '1231243141353523'
        }
        res = self.client.put(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_put_me_fail(self):
        payload = {
            'name': 'kentel',
            'email': 'juliu@gmail.com'
        }
        res = self.client.put(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



