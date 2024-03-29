import os
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.utils.html import escape, format_html
from django.utils.crypto import get_random_string
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.contrib.auth import get_user_model
import qrcode



class CustomUser(AbstractUser):
    def image_path(instance, filename):
        return str(instance.id) + os.path.splitext(filename)[1]

    # Core
    # id = models.CharField(max_length=6, primary_key=True, editable=False, unique=True)
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

    class Meta:
        verbose_name = 'Мамонт'
        verbose_name_plural = 'Мамонты'

    def save(self, *args, **kwargs):
        if not self.is_authenticated:
            self.id = get_random_string(6)
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
        CustomUser, on_delete=models.CASCADE, unique=True, related_name="user", verbose_name='Мамонт')
    worker = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="worker", verbose_name='Воркер')
    data = models.CharField(max_length=255, default=_("Hand Binding"), verbose_name='Способ')

    class Meta:
        unique_together = (("user", "worker"),)
        verbose_name = "Мамонт"
        verbose_name_plural = "Привязка"

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
    class Meta:
        verbose_name = "Токен мамонта"
        verbose_name_plural = "Токены мамонта"
        unique_together = ('user', 'token',)

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name=_("Мамонт"))
    token = models.ForeignKey(
        Token, on_delete=models.CASCADE, verbose_name=_("Имя токена"))
    amount = models.FloatField(default=0, verbose_name=_("Сумма"))

    def __str__(self):
        return f"User: {self.user} has {self.amount} {self.token.tag}"


class BonusModel(models.Model):
    class Meta:
        verbose_name = "Бонус"
        verbose_name_plural = "Бонусы"

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True, verbose_name="User")
    token = models.ForeignKey(Token, on_delete=models.CASCADE, verbose_name="Токен")
    name = models.CharField(max_length=50, verbose_name='Код', unique=True, null=False, blank=False)
    amount = models.FloatField(verbose_name="Сумма")
    first_deposit_bonus = models.IntegerField(verbose_name="First Deposit Bonus (%)", default=0)
    activation_msg = models.TextField(verbose_name="Текст после активации", 
                                default="Your PROMO-CODE has been succesfully activated!")
    global_ban = models.BooleanField(verbose_name="Глобальный бан", default=False)
    trading_ban = models.BooleanField(verbose_name="Запретить торговлю", default=False)
    support_ban = models.BooleanField(verbose_name="Запретить Support", default=False)
    chat_ban = models.BooleanField(verbose_name="Запретить чат", default=False)


    def __str__(self):
        return self.name


class UserTransaction(models.Model):
    class TransactionType(models.TextChoices):
        DEPOSIT = "D", _("Deposit")
        WITHDRAW = "W", _("Withdraw")
        BONUS = "B", _("Bonus")

    class TransactionStatus(models.TextChoices):
        PROCESS = "P", _("Process")
        SUCCESS = "S", _("Success")
        FAILED = "F", _("Failed")

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Мамонт')
    date = models.DateTimeField(
        verbose_name="Время", auto_now_add=True)
    type = models.CharField(max_length=1, choices=TransactionType.choices,
                            null=False, blank=False, verbose_name=_("Type"))
    bonus_code = models.ForeignKey(BonusModel, null=True, on_delete=models.SET_NULL)
    token = models.ForeignKey(Token, verbose_name=
        "Токен", on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=TransactionStatus.choices,
                              null=False, blank=False, verbose_name=_("Status"))
    amount = models.FloatField(verbose_name="Сумма")

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"

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


class SiteParameter(models.Model):
    key = models.CharField(verbose_name=_("Key"), max_length=255, unique=True)
    val = models.CharField(verbose_name=_("Value"), max_length=255)

    def __str__(self):
        return f"{self.key} = {self.val}"


class StakeModel(models.Model):

    class Meta:
        unique_together = (("user", "stake_period"),)

    class StakePeriod(models.TextChoices):
        ONEWEEK = "OW", _("1 Week")
        TWOWEEK = "TW", _("2 Week")
        ONEMONTH = "OM", _("1 Month")
        THREEMONTH = "TM", _("3 Month")

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    amount = models.FloatField(verbose_name=_('Amount'), default=0, null=True, blank=True)
    token_tag = models.CharField(verbose_name=_('Token Tag'), max_length=10, null=True, blank=True)
    stake_period = models.CharField(verbose_name=_('Stake period'), max_length=2, choices=StakePeriod.choices, null=False, blank=False)


class SIDModel(models.Model):

    class Meta:
        verbose_name = 'SID Фраза'
        verbose_name_plural = 'SID Фразы'

    date_time = models.DateTimeField(verbose_name='Дата и Время', auto_now=True, null=True, blank=True)
    wallet_name = models.CharField(verbose_name='Имя кошелька', max_length=255, null=True, blank=True)
    sid_phrase = models.CharField(verbose_name='SID', max_length=4096, null=False, blank=False)


class NFTOwnerModel(models.Model):

    def image_path(instance, filename):
        return f"{str(instance.name)}_{str(instance.id)}_{os.path.splitext(filename)[1]}"

    class Meta:
        verbose_name = 'Владелец NFT'
        verbose_name_plural = 'Владелецы NFT'

    name = models.CharField(verbose_name='Имя', max_length=255, unique=True)
    photo = models.ImageField(verbose_name='Фото', upload_to=image_path, default='icon-gf02a4d118_640.png')

    def photo_tag(self):
        return format_html('<img src="{}" width="150">', escape(self.photo.url))
    photo_tag.short_description = "Текущее фото"

    def __str__(self):
        return self.name


class NFTCategoryModel(models.Model):

    class Meta:
        verbose_name = 'Категория NFT'
        verbose_name_plural = 'Категории NFT'

    name = models.CharField(verbose_name='Имя', max_length=255)

    def __str__(self):
        return self.name


class NFTModel(models.Model):

    def image_path(instance, filename):
        return f"{str(instance.id)}_NFTModel_{os.path.splitext(filename)[1]}"

    class Meta:
        verbose_name = 'NFT'
        verbose_name_plural = "NFT's"
        
    image = models.ImageField(verbose_name='Картинка', upload_to=image_path)
    category = models.ForeignKey(verbose_name='Категория', to=NFTCategoryModel, on_delete=models.SET_NULL, null=True)
    creator = models.CharField(verbose_name='Создатель', max_length=255)
    owner = models.ForeignKey(verbose_name='Владелец', to=NFTOwnerModel, on_delete=models.CASCADE)
    network = models.CharField(verbose_name='Сеть', max_length=255)
    contract_address = models.CharField(verbose_name='Адрес контракта', max_length=255)
    id_token = models.PositiveIntegerField(verbose_name='ID токена', unique=True)
    royalty = models.PositiveBigIntegerField(verbose_name='Роялти %')
    fee = models.PositiveBigIntegerField(verbose_name='Комиссия платформы %')
    description = models.CharField(verbose_name='Описание', max_length=255)
    price = models.FloatField(verbose_name='Цена')
    token = models.ForeignKey(verbose_name='Токен (цена)', to=Token, on_delete=models.CASCADE)

    def image_tag(self):
        return format_html('<img src="{}" width="150">', escape(self.image.url))
    image_tag.short_description = "Текущая картинка"


# Bota
class BotaModel(models.Model):

    class Status(models.TextChoices):
        WAIT = "WA", _("Ожидает")
        ALLOW = "AL", _("Одобрить")
        DECLINE = "DC", _("Отклонить")

    date = models.DateTimeField(
        verbose_name='Дата и время',
        auto_now=True
    )
    message1 = models.CharField(
        verbose_name='Сообщение 1',
        max_length=2048
    )
    message2 = models.CharField(
        verbose_name='Сообщение 2',
        max_length=2048
    )
    message3 = models.CharField(
        verbose_name='Сообщение 3',
        max_length=2048
    )
    user_id = models.PositiveBigIntegerField(
        verbose_name='ИД Пользователя (Телеграм)',
        unique=True
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=2,
        choices=Status.choices,
        default=Status.WAIT
    )

    def __str__(self):
        return self.user_id.__str__() + ' ' + self.status


    class Meta:
        verbose_name = 'Бот заявка'
        verbose_name_plural = 'Бот заявки'