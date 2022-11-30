from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .utils import DataMixin
from .forms import RegisterUserForm, LoginUserForm
from .models import Token, UserToken


def deposit(request):
    tokens = Token.objects.all()
    result = []

    for token in tokens:
        amount = 0.0
        try:
            user_token = UserToken.objects.get(user=request.user, token=token)
            amount = user_token.amount
        except:
            pass
        result.append(
            {
                'token': token,
                'amount': amount,
            }
        )

    context = {
        "data": result,
    }

    return render(
        request=request,
        template_name="user_profile/deposit.html",
        context=context
    )


def withdraw(request):
    tokens = Token.objects.all()
    result = []

    for token in tokens:
        amount = 0.0
        try:
            user_token = UserToken.objects.get(user=request.user, token=token)
            amount = user_token.amount
        except:
            pass
        result.append(
            {
                'token': token,
                'amount': amount,
            }
        )

    context = {
        "data": result,
    }

    return render(
        request=request,
        template_name="user_profile/withdraw.html",
        context=context
    )


def transactions(request):
    return render(
        request=request,
        template_name="user_profile/transactions.html",
        context=None
    )


def transfer(request):
    return render(
        request=request,
        template_name="user_profile/transfer.html",
        context=None
    )


def invest(request):
    return render(
        request=request,
        template_name="user_profile/invest.html",
        context=None
    )


def affiliate(request):
    return render(
        request=request,
        template_name="user_profile/affiliate.html",
        context=None
    )


def api(request):
    return render(
        request=request,
        template_name="user_profile/api.html",
        context=None
    )


def settings(request):
    return render(
        request=request,
        template_name="user_profile/settings.html",
        context=None
    )


def wallet(request):
    tokens = Token.objects.all()
    result = []

    for token in tokens:
        amount = 0.0
        try:
            user_token = UserToken.objects.get(user=request.user, token=token)
            amount = user_token.amount
        except:
            pass
        result.append(
            {
                'token': token,
                'amount': amount,
            }
        )

    context = {
        "data": result,
    }

    return render(request, "user_profile/wallet.html", context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "user_profile/register.html"
    success_url = reverse_lazy("user_profile:login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Register")
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = "user_profile/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Register")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy("main:index")
