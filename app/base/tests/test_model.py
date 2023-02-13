from django.test import TestCase
from django.contrib.auth import get_user_model
from io import StringIO
from django.core.management import call_command
from django.contrib.auth.models import Group
from base.models import (Ingredient,
                         Function,
                         Unit,
                         Supplier,
                         Pic,
                         IngredientDocument,
                         SupplierDocument, )


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

    def test_ingredient_model_base_successful(self):
        name = 'IngredientA Washed up 500'
        quantity = 1
        price = 10.20
        is_used = True

        ingredient = Ingredient.objects.create(name=name,
                                               quantity=quantity,
                                               price=price,
                                               is_used=is_used)
        self.assertEqual(ingredient.name, name)
        self.assertEqual(ingredient.quantity, quantity)
        self.assertEqual(ingredient.price, price)
        self.assertTrue(ingredient.is_used)

    def test_function_model_successful(self):
        name = 'Hydrochloric Acid'

        function = Function.objects.create(name=name)

        self.assertEqual(function.name, name)

    def test_unit_model_successful(self):
        name = 'ounce'
        abbreviation = 'oz'
        conversion_rate = 28.3

        unit = Unit.objects.create(name=name, abbreviation=abbreviation, conversion_rate=conversion_rate)

        self.assertEqual(unit.name, name)
        self.assertEqual(unit.abbreviation, abbreviation)
        self.assertEqual(unit.conversion_rate, conversion_rate)

    def test_supplier_model_successful(self):
        name = 'Hydrochloric Acid'
        location = 'Bekasi, Indonesia'
        phone = '+62081231235123'

        supplier = Supplier.objects.create(name=name, location=location, phone=phone)

        self.assertEqual(supplier.name, name)
        self.assertEqual(supplier.location, location)
        self.assertEqual(supplier.phone, phone)

    def test_pic_model_successfull(self):
        name = 'sadadsaadasdas'
        position = ' on top of the world baby'
        email = 'clas12345@gmail.com'

        pic = Pic.objects.create(name=name, position=position, email=email)

        self.assertEqual(pic.name, name)
        self.assertEqual(pic.position, position)
        self.assertEqual(pic.email, email)

    def test_ingredient_document_one_connections(self):
        name = 'IngredientA Washed up 500'
        quantity = 1
        price = 10.20
        is_used = True

        ingredient = Ingredient.objects.create(name=name,
                                               quantity=quantity,
                                               price=price,
                                               is_used=is_used)
        document = IngredientDocument.objects.create(ingredient=ingredient)

        self.assertEqual(document.ingredient, ingredient)
        self.assertEqual(ingredient.ingredientdocument, document)

    def test_supplier_document_one_connection(self):
        name = 'Hydrochloric Acid'
        location = 'Bekasi, Indonesia'
        phone = '+62081231235123'
        supplier = Supplier.objects.create(name=name,
                                           location=location,
                                           phone=phone, )
        document = SupplierDocument.objects.create(supplier=supplier)

        self.assertEqual(document.supplier, supplier)
        self.assertEqual(supplier.supplierdocument, document)
