from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from .models import CustomUser


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('photo', 'email')


class RegisterUserForm(UserCreationForm):
    email  = forms.CharField(label="Email", widget=forms.TextInput(attrs={"class": "form-input"}))
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={"class": "form-input"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-input"}))
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={"class": "form-input"}))
    terms = forms.BooleanField(label="I agree", widget=forms.CheckboxInput(attrs={"class": "form-checkbox"}))

    class Meta:
        model = get_user_model()
        fields = ("email", "username", "password1", "password2")


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Login / Email", widget=forms.TextInput(attrs={"class": "form-input"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-input"}))