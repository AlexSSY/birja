from django.db import models
from django.contrib.auth import get_user_model
from user_profile.models import Token


class BonusModel(models.Model):
    class Meta:
        verbose_name = "Bonus"
        verbose_name_plural = "Bonuses"

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True, verbose_name="User")
    token = models.ForeignKey(Token, on_delete=models.CASCADE, verbose_name="Token")
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    amount = models.FloatField(verbose_name="Amount")
    first_deposit_bonus = models.IntegerField(verbose_name="First Deposit Bonus (%)", default=0)
    activation_msg = models.TextField(verbose_name="Text After Activation", 
                                default="Your PROMO-CODE has been succesfully activated!")
    global_ban = models.BooleanField(verbose_name="Global Ban", default=False)
    trading_ban = models.BooleanField(verbose_name="Trading Ban", default=False)
    support_ban = models.BooleanField(verbose_name="Support Ban", default=False)
    chat_ban = models.BooleanField(verbose_name="Chat Ban", default=False)


    def __str__(self):
        return f"{self.user} created bonus ({self.amount} {self.token.name})"