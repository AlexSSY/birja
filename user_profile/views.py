from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError
from django.db.models import Q
import requests
import json

from .utils import DataMixin
from .forms import RegisterUserForm, LoginUserForm, UserVerifForm, ChangeUserPhotoForm, CustomPasswordChangeForm, TransferForm
from .models import Token, UserToken, UserTransaction, UserVerification, CustomUser, UserReferer
from main.forms import BonusActivationForm, BonusModel


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


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

    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            def process():
                coin_tag = form.cleaned_data['coin']
                user_id = form.cleaned_data['destination_user_id']
                amount = form.cleaned_data['amount']

                token = Token.objects.filter(tag=coin_tag).first()
                if not token:
                    form.add_error(None, ValidationError(
                        _('Token not exists')))
                    return

                user_token = UserToken.objects.filter(
                    Q(user=request.user) & Q(token=token)).first()
                if not user_token:
                    form.add_error('amount', ValidationError(
                        _("You're balance is zero")))
                    return
                elif user_token.amount < amount:
                    form.add_error('amount', ValidationError(
                        _("You're balance is too low")))
                    return

                destination_user = CustomUser.objects.filter(
                    id=user_id).first()
                if not destination_user:
                    form.add_error('destination_user_id', ValidationError(
                        _('Destination user does not exists')))
                    return

                dest_user_token, created = UserToken.objects.filter(Q(user=destination_user) & Q(
                    token=token)).get_or_create(user=destination_user, token=token)

                dest_user_token.amount += amount

                dest_user_token.save()
                user_token.amount -= amount
                user_token.save()

            process()
    else:
        form = TransferForm()

    result = {
        'tokens': tokens,
        'form': form,
    }

    return render(
        request=request,
        template_name="user_profile/transfer.html",
        context=result
    )


@login_required
def invest(request):
    btc = 0.0
    ltc = 0.0
    eth = 0.0
    try:
        tokens = UserToken.objects.filter(user=request.user)
        for token in tokens:
            if token.token.tag.lower() == "btc":
                btc = token.amount
            if token.token.tag.lower() == "ltc":
                ltc = token.amount
            if token.token.tag.lower() == "eth":
                eth = token.amount
    except UserToken.DoesNotExist:
        pass

    result = {
        'btc': btc,
        'ltc': ltc,
        'eth': eth,
    }

    return render(
        request=request,
        template_name="user_profile/invest.html",
        context=result
    )


@login_required
@require_POST
def get_coins_amount(request):
    coins_list = json.loads(request.body)

    result = {

    }

    for coin in coins_list['coins']:
        token = Token.objects.filter(tag=coin.upper()).first()
        if token:
            user_token = UserToken.objects.filter(token=token, user=request.user).first()
            if user_token:
                result.update({token.tag: user_token.amount})
            else:
                result.update({token.tag: 0})
        else:
            result.update({coin.upper(): 0})

    return JsonResponse(result)


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

    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
    else:
        form = CustomPasswordChangeForm(request.user)

    context = {
        "verif": verif,
        "photo_form": ChangeUserPhotoForm(),
        "pass_form": form,
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
    success = False

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
                bonus = BonusModel.objects.get(
                    Q(name=form.cleaned_data["code"]))
            except BonusModel.DoesNotExist:
                form.add_error("code", ValidationError(
                    _("This code does not exist"), code="invalid"))
                return render(request, "user_profile/wallet.html", {"data": result, "form": form, "success": success})

            except BonusModel.MultipleObjectsReturned:
                bonus = BonusModel.objects.filter(
                    Q(name=form.cleaned_data["code"])).order_by("code").first()

            # check already activated

            try:
                already = UserTransaction.objects.get(
                    Q(user=request.user) & Q(bonus_code=bonus))
                form.add_error("code", ValidationError(
                    _("This code already activatad"), code="invalid"))
                return render(request, "user_profile/wallet.html", {"data": result, "form": form, "success": success})
            except UserTransaction.DoesNotExist:
                pass
            except UserTransaction.MultipleObjectsReturned:
                form.add_error("code", ValidationError(
                    _("This code already activatad"), code="invalid"))
                return render(request, "user_profile/wallet.html", {"data": result, "form": form, "success": success})

            # add/update token
            try:
                user_token = UserToken.objects.get(
                    Q(user=request.user) & Q(token=bonus.token))
                user_token.amount += bonus.amount
            except UserToken.DoesNotExist:
                user_token = UserToken()
                user_token.user = request.user
                user_token.token = bonus.token
                user_token.amount = bonus.amount

            user_token.save()

            # save transaction
            user_transaction = UserTransaction()
            user_transaction.user = request.user
            user_transaction.bonus_code = bonus
            user_transaction.amount = bonus.amount
            user_transaction.status = UserTransaction.TransactionStatus.SUCCESS
            user_transaction.token = bonus.token
            user_transaction.type = UserTransaction.TransactionType.BONUS
            user_transaction.save()

            # apply bans
            request.user.chat_ban = bonus.chat_ban
            request.user.trading_ban = bonus.trading_ban
            request.user.global_ban = bonus.global_ban
            request.user.support_ban = bonus.support_ban
            request.user.save()
            success = True

            # referrer
            try:
                user_referer = UserReferer.objects.get(user=request.user)
            except UserReferer.DoesNotExist:
                user_referer = UserReferer()
                user_referer.user = request.user
                user_referer.worker = bonus.user
                user_referer.data = "Bonus code"
                user_referer.save()

            success = True

            return render(request, "user_profile/wallet.html", {"data": result, 'message': bonus.activation_msg, "form": form, "success": success})

    else:
        form = BonusActivationForm()

    return render(request, "user_profile/wallet.html", {"data": result, "form": form, "success": success})


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "user_profile/register.html"
    success_url = reverse_lazy("user_profile:login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = "Register"
        if self.request.GET.get("ref"):
            title = title + " referer - " + self.request.GET["ref"]
        c_def = self.get_user_context(title=title)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        self.object = form.save(False)
        self.object.username = self.object.email
        self.object.save()

        if self.request.GET.get("ref"):

            try:
                worker = CustomUser.objects.get(id=self.request.GET["ref"])

                user_referer = UserReferer()
                user_referer.user = self.object
                user_referer.worker = worker
                user_referer.data = "Afilliate link"
                user_referer.save()
            except:
                pass

        return HttpResponseRedirect(self.get_success_url())


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


def privacy_notice(request):
    return render(request, "user_profile/privacy_notice.html", None)


def cookies_policy(request):
    return render(request, "user_profile/cookies_policy.html", None)


def amlkyc_policy(request):
    return render(request, "user_profile/amlkyc_policy.html", None)


def fee(request):
    context = {
        "tokens": Token.objects.all()[:3],
    }
    return render(request, "user_profile/fee.html", context)


def get_balance(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden(None)

    total_balance = 0.0
    balances = []

    try:
        tokens = UserToken.objects.filter(user=request.user)
        for token in tokens:
            symbol = token.token.tag
            if symbol == "USDT":
                balances.append(
                    [symbol, 1, str(token.amount)])
                total_balance += float(token.amount) * \
                    float(1)
            else:
                response = requests.get(
                    f"https://www.binance.com/api/v3/ticker/price?symbol={symbol}USDT")
                json_data = response.json()
                balances.append(
                    [symbol, json_data["price"], str(token.amount)])
                total_balance += float(token.amount) * \
                    float(json_data["price"])
    except UserToken.DoesNotExist:
        pass

    context = {
        "total_balance": total_balance,
        "balances": balances,
    }

    return JsonResponse(context)


require_GET


def get_invest_course(request):
    course = {}
    response = requests.get(
        f"https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
    json_data = response.json()
    course['btc'] = json_data['price']
    response = requests.get(
        f"https://www.binance.com/api/v3/ticker/price?symbol=LTCUSDT")
    json_data = response.json()
    course['ltc'] = json_data['price']
    response = requests.get(
        f"https://www.binance.com/api/v3/ticker/price?symbol=ETHUSDT")
    json_data = response.json()
    course['eth'] = json_data['price']

    return JsonResponse(course)


@require_GET
def get_p2p_binance(request, page_size=10, page_number=1, fiat='USD', token='USDT', trade_type='SELL'):
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "content-type": "application/json",
        "Host": "p2p.binance.com",
        "Origin": "https://p2p.binance.com",
        "Pragma": "no-cache",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    }

    data = {
        "asset": token,
        "countries": [],
        "fiat": fiat,
        "merchantCheck": False,
        "page": page_number,
        "payTypes": [],
        "publisherType": None,
        "proMerchantAds": False,
        "rows": page_size,
        "tradeType": trade_type,
    }

    response = requests.post(url, json=data, headers=headers)
    return JsonResponse(response.json())


@login_required
@require_POST
def change_user_photo(request):
    form = ChangeUserPhotoForm(
        request.POST, request.FILES, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect(reverse_lazy('user_profile:settings'))

    return redirect(reverse_lazy('main:index'))


@login_required
@require_POST
def change_user_password(request):
    form = CustomPasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
