from django.contrib.auth.models import AbstractUser
from django.db import models
import phonenumber_field.modelfield
from phonenumber_field.formfields import PhoneNumberField


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=30, null=True, verbose_name='username')
    email = models.EmailField(unique=True, max_length=254, null=True, verbose_name='email address')
    first_name = models.CharField(max_length=255, blank=False, null=False, verbose_name='first name')
    last_name = models.CharField(max_length=255, blank=False, null=False, verbose_name='last name')
    phone_number = PhoneNumberField(max_length=11)
    city = models.CharField(max_length=255,)
    avatar = models.ImageField(upload_to='avatars/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'



    def __str__(self):
        return self.email




# Create your models here.
