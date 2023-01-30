from django.test import TestCase
from django.contrib.auth import get_user_model
from io import StringIO
from django.core.management import call_command
from django.contrib.auth.models import Group


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


class ModelTestCase(TestCase):
    def test_create_user_successful(self):
        name = 'julius'
        email = 'juliussutandi@gmail.com'
        password = 'testing1sada1'
        user = create_user()
        self.assertEqual(user.name, name)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_super_user_succesful(self):
        email = 'juliussutandi1@gmail.com'
        password = 'testing1sada1'
        user = create_super_user()
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_groups_succesful(self):
        out = StringIO()
        call_command('create_groups', stdout=out)
        groups = Group.objects.all()

        self.assertIn('Successfully initialized groups', out.getvalue())
        self.assertEqual(groups.count(), 2)

    def test_multiple_create_groups_not_duplicate(self):
        out = StringIO()
        call_command('create_groups', stdout=out)
        self.assertIn('Successfully initialized groups', out.getvalue())
        call_command('create_groups', stdout=out)
        self.assertIn('Successfully initialized groups', out.getvalue())
        groups = Group.objects.all()
        self.assertEqual(groups.count(), 2)
        self.assertNotEqual(groups.count(), 4)

    def test_viewer_permission_check(self):
        user1 = create_user()
        user2 = get_user_model().objects.create_user(name='otong',
                                                     password='test',
                                                     email='hellow@gmail.com')
        viewer_group, created = Group.objects.get_or_create(name="viewer")
        editor_group, created = Group.objects.get_or_create(name="editor")
        user1.groups.add(viewer_group)
        self.assertIn(viewer_group, user1.groups.all())
        self.assertNotIn(editor_group, user1.groups.all())
        user2.groups.add(viewer_group, editor_group)
        self.assertIn(viewer_group, user2.groups.all())
        self.assertIn(editor_group, user2.groups.all())
