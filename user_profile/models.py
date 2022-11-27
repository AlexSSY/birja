import os
from django.utils.translation import gettext as _
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    def image_path(instance, filename):
        return str(instance.id) + os.path.splitext(filename)[1]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=image_path)
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


class Token(models.Model):
    name = models.CharField(max_length=255, null=False, verbose_name=_("Name"))
    tag = models.CharField(max_length=25, null=False, verbose_name=_("Tag"))
    address = models.CharField(max_length=510, null=False, verbose_name=_("Address for deposit(Your Trust Wallet token)"))
    icon = models.FileField(null=False, verbose_name=_("Icon"))

    def __str__(self):
        return f"{self.name} ({self.tag})"


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User name"))
    token = models.ForeignKey(Token, on_delete=models.CASCADE, verbose_name=_("Token name"))
    amount = models.FloatField(default=0, verbose_name=_("Amount"))

    def __str__(self):
        return _(f"User: {self.user} has {self.amount} {self.token.tag}")