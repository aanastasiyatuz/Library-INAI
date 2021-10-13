from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, last_name, group, phone, password, **extra_fields):
        if not username: raise ValueError('username is required')
        if not last_name: raise ValueError('last_name is required')
        if not group: raise ValueError('group is required')
        if not phone: raise ValueError('phone is required')

        user = self.model(username=username,last_name=last_name,group=group,phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    username = models.CharField(max_length=155, unique=True)
    last_name = models.CharField(max_length=155)
    group = models.CharField(max_length=50)
    phone = PhoneNumberField()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['group']

    objects = MyUserManager()

    def __str__(self):
        if self.is_superuser:
            return f"{self.group}: {self.username}"
        return f'{self.group}: {self.last_name} {self.username[0].upper()}.'
