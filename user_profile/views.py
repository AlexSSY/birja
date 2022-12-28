from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError
from django.db.models import Q
import requests
from .utils import DataMixin
from .forms import RegisterUserForm, LoginUserForm, UserVerifForm
from .models import Token, UserToken, UserTransaction, UserVerification, CustomUser
from main.forms import BonusActivationForm, BonusModel


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
    
    try:
        verif = UserVerification.objects.get(user=request.user.id)
    except UserVerification.MultipleObjectsReturned:
        verif = UserVerification.objects.last()
    except UserVerification.DoesNotExist:
        verif = None

    context = {
        "verif": verif,
    }

    return render(
        request=request,
        template_name="user_profile/settings.html",
        context=context
    )


@login_required
def verif(request):
    if request.method == "POST":

        form = UserVerifForm(request.POST, request.FILES)

        try:
            last_verif = UserVerification.objects.get(user=request.user)
            if last_verif.status == UserVerification.Status.BAD:
                last_verif.delete()
            else:
                form.add_error(None, "Verif is already exists")
        except UserVerification.DoesNotExist:
            pass
        except:
            pass

        if form.is_valid():
            verif = form.save(commit=False)
            verif.user = CustomUser.objects.get(id=request.user.id)
            verif.save()
    else:
        form = UserVerifForm()

    context = {
        "form": form,
        "title": "User Verification",
    }

    return render(request, "user_profile/verif.html", context)


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

    if request.method == "POST":
        form = BonusActivationForm(request.POST)
        if form.is_valid():
            try:
                bonus = BonusModel.objects.get(Q(code=form.cleaned_data.code))
            except BonusModel.DoesNotExist:
                form.add_error("code", ValidationError(
                    _("This code does not exist"), code="invalid"))
            except BonusModel.MultipleObjectsReturned:
                bonus = BonusModel.objects.filter(
                    Q(code=form.cleaned_data.code)).order_by("code").first()

            # add/update token

            # apply bans

    else:
        form = BonusActivationForm()

    context = {
        "data": result,
        "form": form,
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


def get_balance(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden(None)

    total_balance = 0.0
    balances = []

    try:
        tokens = UserToken.objects.filter(user=request.user)
        for token in tokens:
            symbol = token.token.tag
            response = requests.get(f"https://api.binance.com/api/v1/ticker/24hr?symbol={symbol}USDT")
            json_data = response.json()
            balances.append([symbol, json_data["lastPrice"], str(token.amount)])
            total_balance += float(token.amount) * float(json_data["lastPrice"])
    except UserToken.DoesNotExist:
        pass

    context = {
        "total_balance": total_balance,
        "balances": balances,
    }

    return JsonResponse(context)