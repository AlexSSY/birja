import os
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import qrcode


class CustomUser(AbstractUser):
    def image_path(instance, filename):
        return str(instance.id) + os.path.splitext(filename)[1]

    # Core
    email = models.EmailField(_("Email"), unique=True)

    # UserProfile
    photo = models.ImageField(upload_to=image_path,
                              default="icon-gf02a4d118_640.png")
    postal_code = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=256, null=True, blank=True)
    city = models.CharField(max_length=256, null=True, blank=True)
    present_address = models.CharField(max_length=256, null=True, blank=True)
    permanent = models.CharField(max_length=256, null=True, blank=True)
    phone_number = models.CharField(max_length=128, null=True, blank=True)

    # Bans
    global_ban = models.BooleanField(_("Global BAN"), default=False)
    trading_ban = models.BooleanField(_("Trading BAN"), default=False)
    chat_ban = models.BooleanField(_("Chat BAN"), default=False)
    support_ban = models.BooleanField(_("Support BAN"), default=False)

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.photo.path)
        width, height = img.size  # Get dimensions

        if width > 300 and height > 300:
            # keep ratio but shrink down
            img.thumbnail((width, height))

        # check which one is smaller
        if height < width:
            # make square by cutting off equal amounts left and right
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))

        elif width < height:
            # make square by cutting off bottom
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 300 and height > 300:
            img.thumbnail((300, 300))

        img.save(self.photo.path)


class UserReferer(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="user")
    worker = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="worker")
    data = models.CharField(max_length=255, default=_("Hand Binding"))

    class Meta:
        unique_together = (("user", "worker"),)


class UserVerification(models.Model):

    class IDType(models.TextChoices):
        DRIVER_LICENSE = "DL", _("Dirver License")
        ID_CARD = "IC", _("ID Card")
        PASSPORT = "PS", _("Passport")

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    document_photo = models.ImageField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    id_number = models.IntegerField()
    id_type = models.CharField(
        max_length=2, choices=IDType.choices, default=IDType.DRIVER_LICENSE)


class Token(models.Model):
    name = models.CharField(max_length=255, null=False, verbose_name=_("Name"))
    tag = models.CharField(max_length=25, null=False, verbose_name=_("Tag"))
    address = models.CharField(
        max_length=510, null=False, verbose_name=_("Address for deposit"))
    icon = models.FileField(null=False, verbose_name=_("Icon"))
    qr_code = models.ImageField(upload_to="qr_codes", blank=True)

    def __str__(self):
        return f"{self.name} ({self.tag})"

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.address)
        canvas = Image.new('RGB', (qrcode_img.pixel_size,
                           qrcode_img.pixel_size), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f"qr_code-{self.address}.png"
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


class UserToken(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name=_("User name"))
    # user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    token = models.ForeignKey(
        Token, on_delete=models.CASCADE, verbose_name=_("Token name"))
    # token = models.OneToOneField(to=Token, on_delete=models.CASCADE)
    amount = models.FloatField(default=0, verbose_name=_("Amount"))

    def __str__(self):
        return _(f"User: {self.user} has {self.amount} {self.token.tag}")


class UserTransaction(models.Model):
    class TransactionType(models.TextChoices):
        DEPOSIT = "D", _("Deposit")
        WITHDRAW = "W", _("Withdraw")
        BONUS = "B", _("Bonus")

    class TransactionStatus(models.TextChoices):
        PROCESS = "P", _("Process")
        SUCCESS = "S", _("Success")
        FAILED = "F", _("Failed")

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(
        verbose_name=_("Date & Time"), auto_now_add=True)
    type = models.CharField(max_length=1, choices=TransactionType.choices,
                            null=False, blank=False, verbose_name=_("Type"))
    bonus_code = models.CharField(max_length=50, null=True, blank=True)
    token = models.ForeignKey(Token, verbose_name=_(
        "Token"), on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=TransactionStatus.choices,
                              null=False, blank=False, verbose_name=_("Status"))
    amount = models.FloatField(verbose_name=_("Amount"))

    def __str__(self):
        return f"{self.user} - {self.type}: {self.token} {self.amount}"
