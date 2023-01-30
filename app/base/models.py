from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.contrib.auth.models import Group

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
    name = models.CharField(max_length=255, null=True, blank=True )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    objects = MyUserManager()
    groups = models.ManyToManyField(Group, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


