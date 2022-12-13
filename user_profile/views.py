from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .utils import DataMixin
from .forms import RegisterUserForm, LoginUserForm
from .models import Token, UserToken, UserTransaction


@login_required
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


@login_required
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


@login_required
def transactions(request):
    result = []
    context = None

    try:
        transactions = UserTransaction.objects.filter(user=request.user)

        for transaction in transactions:
            data = {
                'id': transaction.id,
                'date': transaction.date,
                'type': transaction.get_type_display(),
                'amount': transaction.amount,
                'token': transaction.token,
                'status': transaction.get_status_display(),
                'balance': 0.0,
            }

            result.append(
                {
                    'transaction': data,
                }
            )

        context = {
            "data": result,
        }
    except Exception as e:
        pass

    return render(
        request=request,
        template_name="user_profile/transactions.html",
        context=context
    )


@login_required
def transfer(request):
    tokens = Token.objects.all()

    result = {
        'tokens': tokens,
    }

    return render(
        request=request,
        template_name="user_profile/transfer.html",
        context=result
    )


@login_required
def invest(request):
    tokens = Token.objects.all()

    result = {
        'tokens': tokens,
    }

    return render(
        request=request,
        template_name="user_profile/invest.html",
        context=result
    )


@login_required
def affiliate(request):
    return render(
        request=request,
        template_name="user_profile/affiliate.html",
        context=None
    )


@login_required
def api(request):
    return render(
        request=request,
        template_name="user_profile/api.html",
        context=None
    )


@login_required
def settings(request):
    return render(
        request=request,
        template_name="user_profile/settings.html",
        context=None
    )


@login_required
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
        c_def = self.get_user_context(title="Login")
        return dict(list(context.items()) + list(c_def.items()))


@login_required
def custom_logout(request):
    logout(request)
    return redirect(reverse_lazy("main:index"))

def terms(request):
    return render(request, "user_profile/terms.html", None)