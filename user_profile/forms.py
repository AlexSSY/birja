from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model, password_validation
from django import forms
from django.forms import ValidationError
from .models import CustomUser, UserVerification
from django.utils.translation import gettext_lazy as _


class UserVerifForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255, widget=forms.TextInput({
        "class": "verif__input",
        "placeholder": _("Johny"),
    }))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput({
        "class": "verif__input",
        "placeholder": _("Maveric"),
    }))
    middle_name = forms.CharField(max_length=255, widget=forms.TextInput({
        "class": "verif__input",
        "placeholder": _("Albert"),
    }))
    date_of_birth = forms.DateField(widget=forms.DateInput({
        "class": "verif__date",
        "type": "date",
        "placeholder": _("01-12-2002"),
    }))
    id_number = forms.IntegerField(widget=forms.NumberInput({
        "class": "verif__input",
        "placeholder": _("000-000-00-00"),
    }))
    id_type = forms.ChoiceField(
        choices=UserVerification.IDType.choices,
        widget=forms.Select(
            {
                "class": "verif__select",
            }
        )
    )
    document_photo = forms.ImageField(widget=forms.FileInput({
        "class": "verif__file",
    }))

    class Meta:
        model = UserVerification
        fields = (
            "first_name",
            "last_name",
            "middle_name",
            "date_of_birth",
            "id_number",
            "id_type",
            "document_photo",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('photo', 'email', )



class RegisterUserForm(UserCreationForm):
    email = forms.CharField(label="Email", widget=forms.TextInput(
        attrs={"class": "form-input"}))
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-input"}))
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(
        attrs={"class": "form-input"}))
    terms = forms.BooleanField(label="I agree", widget=forms.CheckboxInput(
        attrs={"class": "form-checkbox"}))

    class Meta:
        model = get_user_model()
        fields = ("email", "password1", "password2")


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="Email", widget=forms.TextInput(attrs={"class": "form-input"}))
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-input"}))


class SwapForm(forms.Form):
    from_ = forms.CharField(widget=forms.HiddenInput())
    to = forms.CharField(widget=forms.HiddenInput())
    amount = forms.FloatField(min_value=0, label="Amount", widget=forms.NumberInput(attrs={
        "class": "swap__input",
        "placeholder": _("Amount"),
        }
    ))

    def clean_amount(self):
       amount = self.cleaned_data["amount"]
       if amount <= 0:
            raise ValidationError(_("Amount must be higher then zero"))
       return amount


class ChangeUserPhotoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('photo', )
    
    photo = forms.ImageField(allow_empty_file=False, required=True, widget=forms.FileInput(attrs={
        'class': 'settings__form-file',
    }))


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True, "class": "settings__form-text"}
        ),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "settings__form-text"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "settings__form-text"}),
    )


class TransferForm(forms.Form):
    coin = forms.CharField(max_length=50, required=True, widget=forms.HiddenInput())
    destination_user_id = forms.IntegerField(min_value=1, required=True, widget=forms.NumberInput(attrs={
        'placeholder': _('Please enter a destination User ID'),
    }))
    amount = forms.FloatField(min_value=0, required=True, widget=forms.NumberInput(attrs={
        'placeholder': _('Please enter an amount'),
        'step': 'any',
    }))

    def clean_amount(self):
        data = self.cleaned_data['amount']
        if data == 0:
            raise ValidationError(_('Amount must be higher than zero'))
        return data