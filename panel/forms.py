from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from main.models import BonusModel
from user_profile.models import Token


class EmailBinderForm(forms.Form):
    user_email = forms.EmailField(
        max_length=255,
        label=_("Email"),
        widget=widgets.EmailInput(
            {
                "class": "form-control",
                "placeholder": _("Enter user email")
            }
        ))


class PromoBindingForm(forms.ModelForm):
    class Meta:
        model = BonusModel
        fields = ("name", "amount", "first_deposit_bonus", "token")

    name = forms.CharField(
        max_length=255, label=_("Promo"),
        widget=widgets.TextInput(
            {
                "class": "form-control",
                "placeholder": _("Enter promo code")
            }
        ))
    amount = forms.FloatField(
        label=_("Amount"),
        widget=widgets.NumberInput(
            {
                "class": "form-control",
                "placeholder": _("0.01")
            }
        ))
    first_deposit_bonus = forms.IntegerField(
        min_value=0,
        max_value=100,
        label=_("First Deposit Bonus (%)"),
        widget=widgets.NumberInput(
            {
                "class": "form-control",
                "placeholder": _("50%")
            }
        ))
    token = forms.ModelChoiceField(
        queryset=Token.objects.all(),
        widget=widgets.Select(
            {
                "class": "form-select",
            }
        )
    )
    activation_msg = forms.CharField(
        label=_("Text After Activation"),
        widget=widgets.Textarea(
            {
                "class": "form-control",
            }
        )
    )
    global_ban = forms.BooleanField(
        label=_("Global BAN"),
        widget=widgets.CheckboxInput(
            {
                "class": "form-check-input",
            }
        )
    )
    trading_ban = forms.BooleanField(
        label=_("Trading BAN"),
        widget=widgets.CheckboxInput(
            {
                "class": "form-check-input",
            }
        )
    )
    support_ban = forms.BooleanField(
        label=_("Support BAN"),
        widget=widgets.CheckboxInput(
            {
                "class": "form-check-input",
            }
        )
    )
    chat_ban = forms.BooleanField(
        label=_("Chat BAN"),
        widget=widgets.CheckboxInput(
            {
                "class": "form-check-input",
            }
        )
    )
