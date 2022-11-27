from django.shortcuts import render
from django.utils.translation import gettext as _

# Create your views here.
def index(request):
    context = {
        "title": _("Index")
    }
    return render(request, "base.html", context)