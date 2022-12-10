from django import forms


class EmailBinderForm(forms.Form):
    user_email = forms.EmailField(
        max_length=255, label="Email", widget=forms.widgets.EmailInput({"class": "form-control"}))

    # template_name = "panel/default_form_template.html"
