from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, last_name, group, phone, password, **extra_fields):
        if not email: raise ValueError('email is required')
        if not username: raise ValueError('username is required')
        if not last_name: raise ValueError('last_name is required')
        if not group: raise ValueError('group is required')
        if not phone: raise ValueError('phone is required')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, last_name=last_name, group=group, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email: raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)       
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)
    group = models.CharField(max_length=50)
    phone = PhoneNumberField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['usename', 'last_name', 'group']

    objects = MyUserManager()

    def __str__(self):
        if self.is_superuser:
            return f"{self.group}: {self.username}"
        return f'{self.group}: {self.last_name} {self.username[0].upper()}.'
