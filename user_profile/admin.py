from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from user_profile.models import UserProfile, UserVerification, Token, UserToken, UserTransaction


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = _("User Profile")


class UserVerificationInline(admin.StackedInline):
    model = UserVerification
    can_delete = False
    verbose_name = _("User Verification")


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, UserVerificationInline)


# admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)


class UserTokenInline(admin.StackedInline):
    model = UserToken
    can_delete = False
    verbose_name = _("UserToken")


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ("name", "tag", "address")
    inlines = (UserTokenInline,)
    pass


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
