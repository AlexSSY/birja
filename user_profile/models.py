import os
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.utils.html import escape, format_html
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


class G2FA(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gauth_key = models.CharField(max_length=16)


class UserReferer(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, unique=True, related_name="user")
    worker = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="worker")
    data = models.CharField(max_length=255, default=_("Hand Binding"))

    class Meta:
        unique_together = (("user", "worker"),)

    def __str__(self):
        return f"{self.worker.email} ---------> {self.user.email}"


class UserVerification(models.Model):

    class IDType(models.TextChoices):
        DRIVER_LICENSE = "DL", _("Dirver License")
        ID_CARD = "IC", _("ID Card")
        PASSPORT = "PS", _("Passport")

    class Status(models.TextChoices):
        PROCEED = "PC", _("Proceed")
        OK = "OK", _("OK")
        BAD = "BD", _("Bad")

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    document_photo = models.ImageField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    id_number = models.IntegerField()
    id_type = models.CharField(
        max_length=2, choices=IDType.choices, default=IDType.DRIVER_LICENSE)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.PROCEED)

    def document_photo_tag(self):
        return format_html('<img src="{}" width="150">', escape(self.document_photo.url))
    document_photo_tag.short_description = "Document Photo"

    def __str__(self):
        return f"{self.user.email}"


class Token(models.Model):
    name = models.CharField(max_length=255, null=False, verbose_name=_("Name"))
    tag = models.CharField(max_length=25, null=False, verbose_name=_("Tag"))
    address = models.CharField(
        max_length=510, null=False, verbose_name=_("Address for deposit"))
    icon = models.FileField(null=False, verbose_name=_("Icon"))
    qr_code = models.ImageField(upload_to="qr_codes", blank=True)
    fee = models.FloatField(default=0, verbose_name=_("Network Fee"))
    min = models.FloatField(default=0, verbose_name=_("Minimum for Deposit"))

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
        return f"User: {self.user} has {self.amount} {self.token.tag}"


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


class Fiat(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"), unique=True)
    tag = models.CharField(max_length=25, verbose_name=_("Tag"), unique=True)

    def __str__(self):
        return f"{self.tag} ({self.name})"

class P2P(models.Model):
    class PaymentMethod(models.TextChoices):
        WEBMONEY        = "WEB", _("Webmoney")
        CARD_TO_CARD    = "C2C", _("Card to Card")
        ADVCASH         = "ADV", _("Advcash")
        SIM_BALANCE     = "SIM", _("Sim-card balance")
        MASTERCARD      = "MAS", _("MasterCard")
        PAYEER          = "PAY", _("Payeer")
        PERFECT_MONEY   = "PER", _("Perfect Money")
        PAYPAL          = "PPL", _("PayPal")
        PAYSEND         = "PSE", _("Paysend")
        WESTUNION       = "WSU", _("Western Union")
        PRIVAT          = "PRI", _("PrivatBank")
        POKERSTARS      = "POK", _("PokerStars")
        SWIFT           = "SWT", _("SWIFT")
        VISA            = "VSA", _("Visa")
        REVOLUT         = "REV", _("Revolut")
        SBERBANK        = "SBR", _("Sberbank")
        CASH            = "CSH", _("Cash")
        TINKOFF         = "TNK", _("Tinkoff")
        ALPHA           = "ALH", _("Alphabank")
        VTB             = "VTB", _("VTB")
        REIFFEISEN      = "RFF", _("Reiffeisen")
        ROCKET          = "RCK", _("Rocketbank")
        POCHTA          = "PCH", _("Pochta Bank")
        MIR             = "MIR", _("Mir (Payment system)")
        NATIONAL        = "NAT", _("National bank transfer")
        RUSSIAN         = "RSB", _("Russian Standart Bank")
        MTS             = "MTS", _("MTS-bank")
        GAZ             = "GAZ", _("Gazprombank")
        KYKYRYZA        = "KYK", _("Kykyryza nank")
        RNCB            = "RNC", _("RNCB Bank")
        AVANGARD        = "AVG", _("Avangard Bank")
        TOUCH           = "TCH", _("Touch Bank")
        MOSCOW          = "MSK", _("Bank of Moscow")
        QIWI            = "QWI", _("QIWI")
        SBP             = "SBP", _("SBP")
        YOOMONEY        = "YOO", _("YooMoney")
        ROSBANK         = "ROS", _("Rosbank")
        YANDEX          = "YAN", _("Yandex.Money")
        MTSMONEY        = "MTM", _("MTS Money")
        OTKRITIE        = "OTK", _("Otkritie Bank")
        HOME            = "HCB", _("Home Credit Bank")
        SOVCOMBANK      = "SCB", _("Sovcombank")
        PSBANK          = "PSB", _("PS Bank")
        CASH_TO_ATM     = "CAA", _("Cash at ATM")
        RUSAGRBANK      = "RAB", _("Russian Agricultural Bank")
        URALSIB         = "USB", _("Uralsib")
        CREDITMOSCOW    = "CMB", _("Credit Bank of Moscow")
        OTPBANK         = "OTP", _("OTP Bank")
        SAINTBANK       = "BSP", _("Bank Saint Petersburg")
        RENAISSANCE     = "RSC", _("Renaissance Credit")
        UNICREDIT       = "UNI", _("UniCredit Bank")
        CITIBANK        = "CIT", _("Citibank")
        FORBANK         = "FOR", _("ForBank")
        BINANCE         = "BNP", _("BinancePay")
        KORONA          = "KOR", _("KoronaPay (Zolotaya korona)")
        EXODUS          = "EXS", _("Exodus")

    class Status(models.TextChoices):
        ONLINE = "ON", _("Online")
        OFFLINE = "OF", _("Offline")
    
    def image_path(instance, filename):
        return "p2p_" + str(instance.id) + os.path.splitext(filename)[1]

    username = models.CharField(max_length=255, verbose_name=_("User Name"), unique=True)
    photo = models.ImageField(upload_to=image_path, default="icon-gf02a4d118_640.png", verbose_name=_("Photo"))
    orders = models.PositiveIntegerField(verbose_name=_("Orders (count)"))
    orders_percent = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name=_("Orders (percent)"))
    price = models.FloatField(default=0, validators=[MinValueValidator(0)], verbose_name=_("Price"))
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ONLINE, verbose_name=_("Status"))
    method = models.CharField(max_length=3, choices=PaymentMethod.choices, default=PaymentMethod.VISA, verbose_name=_("Payment Method"))
    limit_start = models.FloatField(default=50, validators=[MinValueValidator(0)], verbose_name=_("Limit (start)"))
    limit_end = models.FloatField(default=5000, validators=[MinValueValidator(0)], verbose_name=_("Limit (end)"))
    fiat = models.ForeignKey(Fiat, verbose_name=_("Fiat"), on_delete=models.CASCADE)

    def photo_tag(self):
        return format_html('<img src="{}" width="150">', escape(self.photo.url))
    photo_tag.short_description = "Document Photo"

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

    def __str__(self):
        return f"{self.username} ({self.price})"