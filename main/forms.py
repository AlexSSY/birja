from django import forms
from django.utils.translation import gettext_lazy as _
from .models import BonusModel


class CustomModelForm(forms.ModelForm):
    model = None


class BonusActivationForm(forms.Form):
    code = forms.CharField(max_length=255, required=True, widget=forms.TextInput({
        "class": "form-control",
    }))


class ChatForm(forms.Form):
    message = forms.CharField(max_length=255, required=True, widget=forms.TextInput({
        "class": "trading__chat-input",
        "placeholder": _("message here..."),
    }))