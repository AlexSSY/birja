from django.shortcuts import render
from django.utils.translation import gettext as _


def index(request):
    context = {
        "title": _("Index")
    }
    return render(request, "base.html", context)


def bonus(request, bonus_name):
    pass