from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Gender(models.TextChoices):
    MALE = 'Male', _('Male')
    FEMALE = 'Female', _('Female')
    OTHER = 'Other', _('Other')


class MaritalStatus(models.TextChoices):
    SINGLE = 'Single'
    MARRIED = 'Married'


class UserRoles(models.TextChoices):
    USER = 'User'
    POLICE = 'Police'
    ADMIN = 'Admin'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=30, choices=Gender.choices, blank=True, null=True)
    marital_status = models.CharField(max_length=30, choices=MaritalStatus.choices, blank=True, null=True)
    role = models.CharField(max_length=30, choices=UserRoles.choices, default=UserRoles.USER)

    def __str__(self):
        return f'{self.user.username} Profile'
