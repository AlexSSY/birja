from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from .models import *
from .forms import CustomUserChangeForm


@admin.register(UserVerification)
class UserVerificationAdmin(admin.ModelAdmin):
    model = UserVerification
    list_display = ("user", "status")
    fields = ("document_photo_tag", "first_name", "last_name",
              "middle_name", "date_of_birth", "id_number", "id_type", "status")
    readonly_fields = ("document_photo_tag", "first_name", "last_name",
                       "middle_name", "date_of_birth", "id_number", "id_type")


class UserVerificationInline(admin.StackedInline):
    model = UserVerification
    can_delete = False
    fields = ("document_photo_tag", "first_name", "last_name",
              "middle_name", "date_of_birth", "id_number", "id_type", "status")
    readonly_fields = ("document_photo_tag", "first_name", "last_name",
                       "middle_name", "date_of_birth", "id_number", "id_type")
    verbose_name = _("Verification")


@admin.register(G2FA)
class G2FAAdmin(admin.ModelAdmin):
    model=G2FA
    list_display = ("user", "gauth_key")
    fields = ("user", "gauth_key")
    readonly_fields = ("user", "gauth_key")


class UserG2FAInline(admin.StackedInline):
    model = G2FA
    can_delete = False
    verbose_name = _("2FA auth")


class UserAdmin(admin.ModelAdmin):
    model = CustomUser
    # form = CustomUserChangeForm
    inlines = (UserVerificationInline, UserG2FAInline, )


admin.site.register(CustomUser, UserAdmin)


@admin.register(UserReferer)
class UserRefererAdmin(admin.ModelAdmin):
    model = UserReferer
    verbose_name = _("Referal")


class UserTokenInline(admin.StackedInline):
    model = UserToken
    can_delete = False
    verbose_name = _("UserToken")


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ("name", "tag", "address")
    fields = ("name", "tag", "address", "icon", "fee", "min")
    inlines = (UserTokenInline, )


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'amount')
    list_filter = ("user", "token")
    search_fields = ("User",)


@admin.register(UserTransaction)
class UserTransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "get_type_display",
                    "bonus_code", "token", "get_status_display", "amount")
    readonly_fields = ("date",)


@admin.register(Fiat)
class FiatAdmin(admin.ModelAdmin):
    list_display = ("name", "tag")


@admin.register(P2P)
class P2PAdmin(admin.ModelAdmin):
    fields = ("username", "photo", "orders", "orders_percent", "price", "status", "method",
                "limit_start", "limit_end", "fiat")
    list_display = ("username", "price", "method", "limit_start", "limit_end")