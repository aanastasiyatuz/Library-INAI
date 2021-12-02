from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
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
        user = self.model(email=email, username=username.capitalize(), last_name=last_name.capitalize(), group=group, phone=phone, **extra_fields)
        user.set__password(password)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email: raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)       
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

GROUPS = (
    # 21
    ('AIN-1-21', 'AIN-1-21'),
    ('AIN-2-21', 'AIN-2-21'),
    ('AIN-3-21', 'AIN-3-21'),
    ('WIN-1-21', 'WIN-1-21'),
    ('MIN-1-21', 'MIN-1-21'),
    # 20
    ('AIN-1-20', 'AIN-1-20'),
    ('AIN-2-20', 'AIN-2-20'),
    ('AIN-3-20', 'AIN-3-20'),
    ('WIN-1-20', 'WIN-1-20'),
    ('MIN-1-20', 'MIN-1-20'),
    # 19
    ('AIN-1-19', 'AIN-1-19'),
    ('AIN-2-19', 'AIN-2-19'),
    ('AIN-3-19', 'AIN-3-19'),
    ('WIN-1-19', 'WIN-1-19'),
    ('MIN-1-19', 'MIN-1-19'),
    # 18
    ('AIN-1-18', 'AIN-1-18'),
    ('AIN-2-18', 'AIN-2-18'),
    ('AIN-3-18', 'AIN-3-18'),
    ('WIN-1-18', 'WIN-1-18'),
    ('MIN-1-18', 'MIN-1-18'),
    # admin
    ('admin', 'admin'),
)

class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)
    group = models.CharField(max_length=50, choices=GROUPS)
    phone = PhoneNumberField()
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=20, blank=True)
    s_password = models.CharField(max_length=100, blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'last_name', 'group']

    objects = MyUserManager()

    def __str__(self):
        if self.is_superuser:
            return f"{self.group}: {self.username}"
        return f'{self.group}: {self.last_name} {self.username[0].upper()}.'

    def create_activation_code(self):
        code = get_random_string(length=20, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        self.activation_code = code
    
    def set__password(self, password):
        self.s_password = password

    def get__password(self):
        return self.s_password
