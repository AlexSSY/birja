from django.contrib import admin
from .models import BonusModel


@admin.register(BonusModel)
class BonusModelAdmin(admin.ModelAdmin):
    model = BonusModel
    list_display = ('name', 'token', 'amount')
    fieldsets = [
        (None, {
            "fields": ("name", "token", "amount"),
        }),
    ]

    def save_model(self, request, obj, form, change) -> None:
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()
