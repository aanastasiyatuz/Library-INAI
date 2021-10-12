from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, password, **extra_fields):
        user = self.model(**extra_fields)
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
    group = models.ForeignKey("Group", related_name="students", on_delete=models.DO_NOTHING)
    phone = PhoneNumberField()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['last_name', 'group', 'phone']

    objects = MyUserManager()

    def __str__(self):
        return f'{self.group}: {self.last_name} {self.username[0].upper()}.'


class Group(models.Model):
    slug = models.CharField(max_length=100, primary_key=True)

    def save(self, *args, **kwargs):
        self.slug = self.slug.upper()
        return super().save(*args, **kwargs)
