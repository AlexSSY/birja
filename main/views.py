from django.shortcuts import render, HttpResponse, redirect
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
import requests

from user_profile.models import Token, P2P, Fiat
from .forms import ChatForm


def index(request):
    # context = {
    #     "title": _("Index"),
    # }
    # return render(request, "main/landing.html", context)
    return redirect("main:trading", symbol_source="btc", symbol_dest="usdt")


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


def bonus(request, bonus_name):
    return HttpResponse(bonus_name)


def p2p(request):
    try:
        p2p_list = P2P.objects.all()
    except:
        p2p_list = []
        pass
    try:
        fiat_list = Fiat.objects.all()
    except:
        fiat_list = []
        pass
    try:
        token_list = Token.objects.all()
    except:
        token_list = []
        pass
    context = {
        "p2p_list": p2p_list,
        "fiat_list": fiat_list,
        "token_list": token_list,
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


def swap(request):
    context = {
        "title": "Swap"
    }
    return render(request, "main/swap.html", context)


def chat(request):
    return HttpResponse(requests.get("https://bitlewro.com/ajax/ajax_chat?a=view").content)

@require_POST
def chat_message(request):
    form = ChatForm(request.POST)
    if form.is_valid():
        return HttpResponse("OK")
    else:
        return HttpResponse("BAD")