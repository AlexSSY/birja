from django import forms
from .models import SupportMessage
from django.utils.translation import gettext_lazy as _


class MessageSendForm(forms.ModelForm):

    class Meta:
        model = SupportMessage
        fields = ("message", )

    message = forms.CharField(
        widget=forms.Textarea(
            {
                "class": "support__textarea",
                "placeholder": _("Please type a message"),
                "rows": "1",
            }
        )
    )
