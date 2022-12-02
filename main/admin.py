from django.contrib import admin
from .models import BonusModel
from django.urls import reverse_lazy


@admin.register(BonusModel)
class BonusModelAdmin(admin.ModelAdmin):
    model = BonusModel
    list_display = ('name', 'token', 'amount', "custom")
    fieldsets = [
        (None, {
            "fields": ("name", "token", "amount"),
        }),
    ]

    def custom(self, obj):
        return reverse_lazy("main:bonus", kwargs={'bonus_name': obj.name})

    def save_model(self, request, obj, form, change) -> None:
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()
