from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
import math
from django.contrib.auth.models import Group
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class RoundedDecimalField(models.DecimalField):
    def from_db_value(self, value, expression, connection, context):
        return round(value, 2)

    def to_python(self, value):
        value = round(super().to_python(value), 2)
        return math.ceil(value * 100) / 100


class MyUserManager(BaseUserManager):
    def create_user(self, email, name=None, password=None, *args, **kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
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



