from django.utils.translation import gettext as _
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField()
    postal_code = models.IntegerField()
    country = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    present_address = models.CharField(max_length=256)
    permanent = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=128)


class UserVerification(models.Model):

    class IDType(models.TextChoices):
        DRIVER_LICENSE = "DL", _("Dirver License")
        ID_CARD = "IC", _("ID Card")
        PASSPORT = "PS", _("Passport")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    document_photo = models.ImageField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    id_number = models.IntegerField()
    id_type = models.CharField(max_length=2, choices=IDType.choices, default=IDType.DRIVER_LICENSE)
