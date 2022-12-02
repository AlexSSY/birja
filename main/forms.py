from django import forms

class CustomModelForm(forms.ModelForm):
    model = None