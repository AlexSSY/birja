from django.db import models
from django.contrib.auth import get_user_model
from django.utils.html import escape, format_html
from django.utils.translation import gettext_lazy as _


class SupportMessage(models.Model):
    sender = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="support_sender",
        verbose_name=_("Sender")
    )
    receiver = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE,
        related_name="support_receiver",
        verbose_name=_("Receiver")
    )
    time = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Time")
    )
    message = models.TextField(
        verbose_name=_("Message")
    )

    def get_receiver_tag(self):
        return format_html('<span style="color: red;">{}</span>', escape(self.receiver))
    get_receiver_tag.short_description = "Receiver"

    def __str__(self):
        return f"{self.message}"
