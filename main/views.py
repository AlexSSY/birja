from django.shortcuts import render, HttpResponse, redirect
from django.utils.translation import gettext as _

from user_profile.models import Token


def index(request):
    # context = {
    #     "title": _("Index"),
    # }
    # return render(request, "main/landing.html", context)
    return redirect("main:trading", symbol_source="btc", symbol_dest="usdt")


def trading(request, symbol_source : str, symbol_dest : str):
    tokens = Token.objects.all()

    context = {
        "title": _("Trading"),
        "tokens": tokens,
        "symbol_source": symbol_source.upper(), #BTC
        "symbol_dest": symbol_dest.upper(),   #USDT
    }
    return render(request, "main/trading.html", context)

def bonus(request, bonus_name):
    return HttpResponse(bonus_name)