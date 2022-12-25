from django.shortcuts import render, HttpResponse, redirect
from django.utils.translation import gettext as _
from django.urls import reverse_lazy

from user_profile.models import Token


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
    }
    return render(request, "main/trading.html", context)


def bonus(request, bonus_name):
    return HttpResponse(bonus_name)


def p2p(request):
    return render(request, "main/p2p.html")


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
