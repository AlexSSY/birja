from django.shortcuts import render, HttpResponse
from django.utils.translation import gettext as _


def index(request):
    context = {
        "title": _("Index")
    }
    return render(request, "base.html", context)


def bonus(request, bonus_name):
    return HttpResponse(bonus_name)