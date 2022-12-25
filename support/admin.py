from django.contrib import admin

from .models import SupportMessage


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    pass