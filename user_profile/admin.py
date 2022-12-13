from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from .models import UserVerification, Token, UserToken, UserTransaction, UserReferer, CustomUser
from .forms import CustomUserChangeForm


class UserVerificationInline(admin.StackedInline):
    model = UserVerification
    can_delete = False
    verbose_name = _("User Verification")


class UserAdmin(admin.ModelAdmin):
    model = CustomUser
    # form = CustomUserChangeForm
    inlines = (UserVerificationInline, )


admin.site.register(CustomUser, UserAdmin)

@admin.register(UserReferer)
class UserRefererAdmin(admin.ModelAdmin):
    pass

class UserTokenInline(admin.StackedInline):
    model = UserToken
    can_delete = False
    verbose_name = _("UserToken")


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ("name", "tag", "address")
    inlines = (UserTokenInline,)


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
