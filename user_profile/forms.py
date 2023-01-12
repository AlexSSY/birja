from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
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
