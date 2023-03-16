from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
import math
from django.contrib.auth.models import Group
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid, os
from django.core.validators import FileExtensionValidator


def get_supplier_doc_file_path(instance, filename):
    """Generate a file path based on a UUID and filename."""
    unique_id = str(uuid.uuid4())
    name, ext = os.path.splitext(filename)
    return f'supplier_docs/{unique_id}/{name}_{unique_id}{ext}'

def get_ingredient_doc_file_path(instance, filename):
    """Generate a file path based on a UUID and filename."""
    unique_id = str(uuid.uuid4())
    name, ext = os.path.splitext(filename)
    return f'ingredient_docs/{unique_id}/{name}_{unique_id}{ext}'

class RoundedDecimalField(models.DecimalField):
    def from_db_value(self, value, expression, connection, context):
        return round(value, 2)

    def to_python(self, value):
        value = round(super().to_python(value), 2)
        return math.ceil(value * 100) / 100


class MyUserManager(BaseUserManager):
    def create_user(self, email, name=None, password=None, is_staff=False, *args, **kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            is_staff=is_staff,
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, *args, **kwargs):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    objects = MyUserManager()
    groups = models.ManyToManyField(Group, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Function(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=5)
    conversion_rate = models.DecimalField(max_digits=120, decimal_places=10)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField(max_length=3000)
    phone = PhoneNumberField(null=True, blank=True)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    is_used = models.BooleanField(default=False)
    supplier = models.ForeignKey(Supplier, null=True, on_delete=models.CASCADE)
    function = models.ForeignKey(Function, null=True, on_delete=models.SET_NULL)
    unit = models.ForeignKey(Unit, null=True, on_delete=models.SET_NULL)
    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name


class Pic(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    supplier = models.ForeignKey(Supplier, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-name']


    def __str__(self):
        return self.name


class SupplierDocument(models.Model):
    supplier = models.OneToOneField(
        Supplier,
        on_delete=models.CASCADE,
    )
    isoDocument = models.FileField(null=True,
                                   blank=True,
                                   upload_to=get_supplier_doc_file_path,
                                   validators=[FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')]
                                   )
    gmpDocument = models.FileField(null=True,
                                   blank=True,
                                   upload_to=get_supplier_doc_file_path,
                                   validators=[FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')]
                                   )
    haccpDocument = models.FileField(null=True,
                                     blank=True,
                                     upload_to=get_supplier_doc_file_path,
                                     validators=[FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')]
                                    )

    class Meta:
        pass

    def __str__(self):
        return str(self.supplier) + "  documents"


class IngredientDocument(models.Model):
    ingredient = models.OneToOneField(
        Ingredient,
        on_delete=models.CASCADE,
    )
    isoDocument = models.FileField(null=True,
                                   blank=True,
                                   upload_to=get_ingredient_doc_file_path,
                                   validators=[FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')])
    gmoDocument = models.FileField(null=True,
                                   blank=True,
                                   upload_to=get_ingredient_doc_file_path,
                                   validators=[FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')])
    kosherDocument = models.FileField(null=True,
                                      blank=True,
                                      upload_to=get_ingredient_doc_file_path,
                                      validators=[FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')])
    halalDocument = models.FileField(null=True,
                                     blank=True,
                                     upload_to=get_ingredient_doc_file_path,
                                     validators=[FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')])
    msdsDocument = models.FileField(null=True,
                                    blank=True,
                                    upload_to=get_ingredient_doc_file_path,
                                    validators=[FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')])
    tdsDocument = models.FileField(null=True,
                                   blank=True,
                                   upload_to=get_ingredient_doc_file_path,
                                   validators=[FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')])
    coaDocument = models.FileField(null=True,
                                   blank=True,
                                   upload_to=get_ingredient_doc_file_path,
                                   validators=[FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')])
    allergenDocument = models.FileField(null=True,
                                        blank=True,
                                        upload_to=get_ingredient_doc_file_path,
                                        validators=[FileExtensionValidator(['pdf'], message='Only PDF files are allowed.')])

    class Meta:
        pass

    def __str__(self):
        return str(self.ingredient) + " documents"







