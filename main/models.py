from django.db import models
from django.contrib.auth.models import User
from user_profile.models import Token


class BonusModel(models.Model):
    class Meta:
        verbose_name = "Bonus"
        verbose_name_plural = "Bonuses"

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="User")
    token = models.OneToOneField(Token, on_delete=models.CASCADE, verbose_name="Token")
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    amount = models.FloatField(verbose_name="Amount")

    def __str__(self):
        return f"{self.user} created bonus ({self.amount} {self.token.name})"


class ExtendenBonusModel(BonusModel):
    class Meta:
        proxy = True