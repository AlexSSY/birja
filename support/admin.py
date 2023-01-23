from django.contrib import admin

from .models import SupportMessage


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    model = SupportMessage
    list_display = ("sender", "get_receiver_tag", "message")