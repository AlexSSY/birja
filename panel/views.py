from django.shortcuts import render
from django.contrib.auth.models import User

from .forms import EmailBinderForm


def index(request):
    return render(request, "panel/base.html")

def bind(request):
    return render(request, "panel/bind.html")

def bind_email(request):
    user = None
    error_list = []
    if request.method == "POST":
        form = EmailBinderForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email__exact=form.cleaned_data["user_email"])
            except User.DoesNotExist:
                error_list.append("User with this email not exists :(")
    else:
        form = EmailBinderForm()

    context = {
        "form": form,
        "founded_user": user,
        "error_list": error_list,
    }
    return render(request, "panel/bind_email.html", context)

def bind_promo(request):
    return render(request, "panel/bind_promo.html", {"form": None})