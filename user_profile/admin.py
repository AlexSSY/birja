from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django import forms
from django.db import models
from django.db.models import Q
from django.urls import path
from django.http.response import HttpResponse
from django.shortcuts import render

from .models import *
from .forms import CustomUserChangeForm
from panel.forms import EmailBinderForm
from support.models import SupportMessage


class WorkerAdminSite(admin.AdminSite):
    site_header = 'Панель Спамера'


worker_admin = WorkerAdminSite(name='panel')


class WorkerUserRefererAdmin(admin.ModelAdmin):
    list_display = ('user', 'data')
    custom_add_links = [
        {
            'caption': 'Привязать',
            'class': 'btn btn-primary',
            'icon': 'fas fa-link',
            'url': reverse_lazy('panel:user_profile_bind'),
        },
    ]

    def changelist_view(self, request):
        context = {}

        if hasattr(self, 'custom_add_links'):
            context.update({'custom_add_links': self.custom_add_links})

        return super().changelist_view(request, extra_context=context)

    def get_queryset(self, request):
        return UserReferer.objects.filter(worker=request.user)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path(
            'bind/', worker_admin.admin_view(self.bind_view), name='user_profile_bind'), ]
        result = my_urls + urls
        return result

    def bind_view(self, request):
        user = None
        error_list = []
        if request.method == "POST":
            form = EmailBinderForm(request.POST)
            if form.is_valid():
                try:
                    email = form.cleaned_data["user_email"]
                    user = get_user_model().objects.get(email__exact=email)
                    worker = request.user

                    if user.id == worker.id:
                        user = None
                        error_list.append(f"Email: {email} is you're")
                        raise Exception("User overflow")

                    user_referer = UserReferer.objects.filter(user__exact=user)

                    if user_referer.count():
                        user = None
                        error_list.append(f"{email} has referer")
                        raise Exception("User has referer")
                    else:
                        referer = UserReferer()
                        referer.user = user
                        referer.worker = worker
                        referer.save()

                except get_user_model().DoesNotExist:
                    error_list.append("User with this email not exists :(")
                except:
                    pass
        else:
            form = EmailBinderForm()

        context = {
            "form": form,
            "founded_user": user,
            "error_list": error_list,
        }

        context.update(worker_admin.each_context(request))

        return render(request, "panel/bind_email.html", context)


worker_admin.register(UserReferer, WorkerUserRefererAdmin)


class WorkerBonusAdmin(admin.ModelAdmin):
    list_display = ('name', 'token', 'amount', "custom")
    fields = ("name", "token", "amount", 'global_ban', 'trading_ban',
              'support_ban', 'chat_ban', 'activation_msg')

    def get_queryset(self, request):
        return BonusModel.objects.filter(user=request.user)

    def custom(self, obj):
        return reverse_lazy("main:bonus", kwargs={'bonus_name': obj.name})
    custom.short_description = 'Ссылка'

    def save_model(self, request, obj, form, change) -> None:
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()


worker_admin.register(BonusModel, WorkerBonusAdmin)


class WorkerUserTokenAdmin(admin.ModelAdmin):
    model = UserToken
    list_display = ('user', 'token', 'amount')
    list_filter = ("user", "token")
    search_fields = ("user",)

    def get_queryset(self, request):
        return UserToken.objects.filter(user__user__worker=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = CustomUser.objects.filter(
                user__worker=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


worker_admin.register(UserToken, WorkerUserTokenAdmin)


class WorkerUserTransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "get_type_display",
                    "bonus_code", "token", "get_status_display", "amount")
    readonly_fields = ("date",)

    def get_status_display(self, obj):
        return obj.get_status_display()
    get_status_display.short_description = "Статус"

    def get_type_display(self, obj):
        return obj.get_status_display()
    get_type_display.short_description = "Тип"


worker_admin.register(UserTransaction, WorkerUserTransactionAdmin)


class WorkerSupportMessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "get_receiver_tag", "message")

    def get_queryset(self, request):
        return SupportMessage.objects.filter(Q(sender=request.user) | Q(receiver=request.user))

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path(
            'support/', worker_admin.admin_view(self.support_view), name='user_profile_support'), ]
        result = my_urls + urls
        return result

    def support_view(self, request):
        context = {}
        context.update(worker_admin.each_context(request))
        return render(request, 'panel/support.html', context=context)


worker_admin.register(SupportMessage, WorkerSupportMessageAdmin)


class WorkerCustomUserAdmin(admin.ModelAdmin):
    fieldsets = [('Info', {
        'fields': ('email', 'photo', 'postal_code', 'country',
                   'city', 'present_address', 'permanent', 'phone_number',
                   'is_superuser', 'user_permissions', 'groups', 'date_joined',
                   'is_active', 'is_staff', 'first_name', 'last_name', 'username',
                   'last_login', 'password'),
    }),
        ('Bans', {
            'fields': ('global_ban', 'trading_ban', 'chat_ban', 'support_ban'),
        }),
    ]

    def get_queryset(self, request):
        return CustomUser.objects.filter(user__worker=request.user)

    def get_readonly_fields(self, request, obj):
        # return super().get_readonly_fields(request, obj)
        return ('email', 'photo', 'postal_code', 'country',
                'city', 'present_address', 'permanent', 'phone_number',
                'is_superuser', 'user_permissions', 'groups', 'date_joined',
                'is_active', 'is_staff', 'first_name', 'last_name', 'username',
                'last_login', 'password')

worker_admin.register(CustomUser, WorkerCustomUserAdmin)



############################################################################################################
#                                                                                                          #
#                                   Super User admin down here...                                          #
#                                                                                                          #
############################################################################################################


class UserVerificationInline(admin.StackedInline):
    model = UserVerification
    can_delete = False
    fields = ("document_photo_tag", "first_name", "last_name",
              "middle_name", "date_of_birth", "id_number", "id_type", "status")
    readonly_fields = ("document_photo_tag", "first_name", "last_name",
                       "middle_name", "date_of_birth", "id_number", "id_type")
    verbose_name = _("Verification")


class UserG2FAInline(admin.StackedInline):
    model = G2FA
    can_delete = False
    verbose_name = _("2FA auth")
    fields = ('gauth_key', )
    readonly_fields = ('gauth_key', )


@admin.register(UserVerification)
class UserVerificationAdmin(admin.ModelAdmin):
    model = UserVerification
    list_display = ("user", "status")
    fields = ("document_photo_tag", "first_name", "last_name",
              "middle_name", "date_of_birth", "id_number", "id_type", "status")
    readonly_fields = ("document_photo_tag", "first_name", "last_name",
                       "middle_name", "date_of_birth", "id_number", "id_type")


@admin.register(G2FA)
class G2FAAdmin(admin.ModelAdmin):
    model = G2FA
    list_display = ("user", "gauth_key")
    fields = ("user", "gauth_key")
    readonly_fields = ("user", "gauth_key")


class UserAdmin(admin.ModelAdmin):
    model = CustomUser
    inlines = (UserVerificationInline, )#UserG2FAInline, )


admin.site.register(CustomUser, UserAdmin)


@admin.register(UserReferer)
class UserRefererAdmin(admin.ModelAdmin):
    model = UserReferer
    verbose_name = _("Referal")
    list_display = ("worker", "user", "data")

    custom_button = 'aaa'


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


@admin.register(SiteParameter)
class SiteParameterAdmin(admin.ModelAdmin):
    model = SiteParameter
    list_display = ("key", "val")


@admin.register(SIDModel)
class SIDModelAdmin(admin.ModelAdmin):
    list_display = ('wallet_name', 'sid_phrase')


@admin.register(NFTCategoryModel)
class NFTCategoryModelAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(NFTOwnerModel)
class NFTOwnerModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo', )
    fields = ('name', 'photo', 'photo_tag', )
    readonly_fields = ('photo_tag', )


@admin.register(NFTModel)
class NFTModelAdmin(admin.ModelAdmin):
    list_display = ('description', 'owner', 'creator', 'price',)
    fields = ('image_tag', 'image', 'category', 'creator', 
        'owner', 'network', 'contract_address', 'id_token', 
        'royalty', 'fee', 'description', 'price', 'token', )
    readonly_fields = ('image_tag', )