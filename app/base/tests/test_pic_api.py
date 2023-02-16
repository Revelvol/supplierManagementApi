from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from base.models import Pic, Supplier
from ingredient.serializers import PicSerializer

PIC_URL = reverse('ingredient:pic-list')


def detail_pic_url(pic_id):
    """Create and return a tag detail url."""
    return reverse('ingredient:pic-detail', args=[pic_id])


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


def create_pic():
    name = 'andi1234'
    email = 'test@example.com'
    phone = '+62866094'
    position = 'leader a'
    supplier = create_supplier()
    pic = Pic.objects.create(name=name, email=email, phone=phone, position=position, supplier=supplier)
    return pic


def create_supplier():
    name = 'pT. Supplier A'
    location = 'Indonesia, Jakarta'
    phone = '+628660942'
    supplier = Supplier.objects.create(name=name, location=location, phone=phone)
    return supplier


class PublicTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_public_pic_access_unauthorized(self):
        payload = {
            'name': 'supplier2',
            'position': 'asdasdasd',
            'phone': '+62832154730812430',
            'email': 'test@example.com',
        }
        res = self.client.post(PIC_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_create_pic_successful(self):
        payload = {
            'name': 'bengki',
            'position': 'staff',
            'phone': '+62812312123',
            'email': 'test@example.com',
        }
        res = self.client.post(PIC_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        function = res.data
        for key, value in payload.items():
            if key == 'supplier':
                continue
            self.assertEqual(function[key], value)

    def test_patch_pic_successful(self):
        pic = create_pic()
        payload = {
            'name': 'bengki',
            'position': 'staff',
            'phone': '+62812312123',
        }
        detail_url = detail_pic_url(pic.id)
        res = self.client.patch(detail_url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        pic.refresh_from_db()
        self.assertEqual(pic.name, payload['name'])

    def test_filter_pic_successful(self):
        supplier1 = create_supplier()

        pic1 = Pic.objects.create(name='andi1231232134',
                                  email='tes123t@example.com',
                                  phone='+628661213094',
                                  position='leader a',
                                  supplier=supplier1)
        pic2 = Pic.objects.create(name='andi112312',
                                  email='tes1231t@example.com',
                                  phone='+628660232394',
                                  position='leader b',
                                    )
        params = {
            'supplier_id': f'{supplier1.id}'
        }

        res = self.client.get(PIC_URL, params)

        p1 = PicSerializer(pic1)
        p2 = PicSerializer(pic2)

        self.assertIn(p1.data, res.data)
        self.assertNotIn(p2.data, res.data)

    def test_filter_pic_with_supplier(self):
        supplier1 = create_supplier()

        pic1 = Pic.objects.create(name='andi1231232134',
                                  email='tes123t@example.com',
                                  phone='+628661213094',
                                  position='leader a',
                                  supplier=supplier1)
        pic2 = Pic.objects.create(name='andi112312',
                                  email='tes1231t@example.com',
                                  phone='+628660232394',
                                  position='leader b',
                                    )
        params = {
            'have_supplier':  1,
        }

        res = self.client.get(PIC_URL, params)

        p1 = PicSerializer(pic1)
        p2 = PicSerializer(pic2)

        self.assertIn(p1.data, res.data)
        self.assertNotIn(p2.data, res.data)

    def test_filter_pic_without_supplier(self):
        supplier1 = create_supplier()

        pic1 = Pic.objects.create(name='andi1231232134',
                                  email='tes123t@example.com',
                                  phone='+628661213094',
                                  position='leader a',
                                  supplier=supplier1)
        pic2 = Pic.objects.create(name='andi112312',
                                  email='tes1231t@example.com',
                                  phone='+628660232394',
                                  position='leader b',
                                    )
        params = {
            'have_supplier':  0,
        }

        res = self.client.get(PIC_URL, params)

        p1 = PicSerializer(pic1)
        p2 = PicSerializer(pic2)

        self.assertIn(p2.data, res.data)
        self.assertNotIn(p1.data, res.data)
