from django.shortcuts import render, HttpResponse, redirect
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.db.models import Q
import requests

from user_profile.models import Token, P2P, Fiat, SiteParameter, UserToken, UserTransaction
from .forms import ChatForm
from user_profile.forms import SwapForm


def index(request):
    context = {
        "title": _("Index"),
    }

    tokens = Token.objects.all()

    for token in tokens:
        context.update({
            token.tag: token,
        })

    return render(request, "main/landing.html", context)
    #return redirect("main:trading", symbol_source="btc", symbol_dest="usdt")


def trading(request, symbol_source: str, symbol_dest: str):
    tokens = Token.objects.all()

    context = {
        "title": _("Trading"),
        "tokens": tokens,
        "symbol_source": symbol_source.upper(),  # BTC
        "symbol_dest": symbol_dest.upper(),  # USDT
        "amount": 0.0,
        "form": ChatForm(),
    }
    return render(request, "main/trading.html", context)


@require_POST
def bonus(request, bonus_name):
    return HttpResponse(bonus_name)


def p2p(request):
    try:
        p2p_list = P2P.objects.all()
    except:
        p2p_list = []
    try:
        fiat_list = Fiat.objects.all()
    except:
        fiat_list = []
    
    token_tags = [
        'USDT', 'BTC', 'BUSD', 'BNB', 'ETH', 'SHIB',
    ]

    try:
        token_list = Token.objects.all();
        tokens = []
        for token in token_list:
            if token.tag in token_tags:
                tokens.append(token)
    except:
        token_list = []
    context = {
        "p2p_list": p2p_list,
        "fiat_list": fiat_list,
        "token_list": tokens,
        "payment_methods": P2P.PaymentMethod.choices,
    }
    return render(request, "main/p2p.html", context)


def market_tools(request):
    return redirect(reverse_lazy("main:market_cap"))


def crypto_market_cap(request):
    context = {
        "title": "Market tools"
    }
    return render(request, "main/crypto_market_cap.html", context)


def market_screener(request):
    context = {
        "title": "Market tools"
    }
    return render(request, "main/market_screener.html", context)


def market_tech(request):
    context = {
        "title": "Market tools"
    }
    return render(request, "main/market_tech.html", context)


def market_cross(request):
    context = {
        "title": "Market tools"
    }
    return render(request, "main/market_cross.html", context)


def market_heat(request):
    context = {
        "title": "Market tools"
    }
    return render(request, "main/market_heat.html", context)


@login_required
def swap(request):
    try:
        tokens = Token.objects.all()
    except Exception as e:
        tokens = []

    if request.method == "POST":
        form = SwapForm(request.POST)
        if form.is_valid():
            from_ = form.cleaned_data["from_"].upper()
            to = form.cleaned_data["to"].upper()
            amount = form.cleaned_data["amount"]

            # Check if from_ == to
            if from_ == to:
                form.add_error("from_", _("From is the same like To"))
                form.add_error("to", _("To is the same like From"))
                return False

            def process():
                # Check if from_ token exist
                try:
                    from_token = Token.objects.get(tag=from_)
                except Token.DoesNotExist as e:
                    form.add_error("from_", ValidationError(
                        _("Token: {from_} does not exist").format(from_=from_)))
                    return False

                # Check if to token exist
                try:
                    to_token = Token.objects.get(tag=to)
                except Token.DoesNotExist:
                    form.add_error("to", ValidationError(
                        _("Token: {to} does not exist").format(to=to)))
                    return False
                
                # Chack UserToken balance
                try:
                    user_token = UserToken.objects.get(
                        Q(user=request.user) & Q(token=from_token))

                    if user_token.amount < amount:
                        form.add_error("from_", ValidationError(
                        _("You have no funds")))
                        return False
                except UserToken.DoesNotExist:
                    form.add_error("from_", ValidationError(
                        _("You have no funds")))
                    return False

                # Get exchange Price
                try:
                    exchange_info = requests.get(f"https://www.binance.com/api/v3/ticker/price?symbol={from_}{to}").json()
                    exchange_price = float(exchange_info["price"])
                except Exception as e:
                    form.add_error(None, ValidationError(e))
                    return False

                # Create / Update destination (UserToken)
                try:
                    dest_user_token = UserToken.objects.get(token=to_token)
                except UserToken.DoesNotExist:
                    dest_user_token = UserToken()
                    dest_user_token.token = to_token
                finally:
                    dest_user_token.user = request.user
                    dest_user_token.amount = exchange_price * amount
                    dest_user_token.save()

                # Decrement UserTiken amount (from)
                user_token.amount = user_token.amount - amount
                user_token.save()

                # Create Transactions

                # Withdraw
                withdraw = UserTransaction()
                withdraw.user = request.user
                withdraw.amount = amount
                withdraw.status = UserTransaction.TransactionStatus.SUCCESS
                withdraw.token = from_token
                withdraw.type = UserTransaction.TransactionType.WITHDRAW
                withdraw.save()

                # Deposit
                deposit = UserTransaction()
                deposit.user = request.user
                deposit.amount = dest_user_token.amount
                deposit.status = UserTransaction.TransactionStatus.SUCCESS
                deposit.token = to_token
                deposit.type = UserTransaction.TransactionType.DEPOSIT
                deposit.save()

            process()
    else:
        form = SwapForm(initial={
            "from_": "BTC",
            "to": "USDT",
        })

    context = {
        "title": "Swap",
        "tokens": tokens,
        "form": form,
    }

    return render(request, "main/swap.html", context)


def chat(request):
    url = SiteParameter.objects.filter(key="bitlerdo_chat").first()
    if url is None:
        return HttpResponse(f'<p>No chat url</p>')
    try:
        data = requests.get(url.val).content
    except Exception as e:
        return HttpResponse(f"<p>{e}</p>")

    return HttpResponse(data)


@require_POST
def chat_message(request):
    form = ChatForm(request.POST)
    if form.is_valid():
        return HttpResponse("OK")
    else:
        return HttpResponse("BAD")
