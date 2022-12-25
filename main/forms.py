from django import forms
from .models import BonusModel


class CustomModelForm(forms.ModelForm):
    model = None


class BonusActivationForm(forms.Form):
    code = forms.CharField(max_length=255, required=True, widget=forms.TextInput({
        "class": "form-control",
    }))
