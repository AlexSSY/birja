from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required

from .forms import EmailBinderForm, PromoBindingForm, MessageSendPanelForm
from user_profile.models import UserReferer
from user_profile.models import BonusModel
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.db.models import Q


@login_required(login_url=reverse_lazy("user_profile:login"))
@permission_required("can_acces_panel")
def index(request):
    return render(request, "panel/base.html")


@login_required(login_url='/accounts/login/')
@permission_required("can_acces_panel")
def bind(request):
    referals = None

    try:
        referals = UserReferer.objects.filter(worker__exact=request.user)
    except:
        pass

    context = {
        "referals": referals,
    }
    return render(request, "panel/bind.html", context)


@login_required(login_url='/accounts/login/')
@permission_required("can_acces_panel")
def bind_email(request):
    user = None
    error_list = []
    if request.method == "POST":
        form = EmailBinderForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data["user_email"]
                user = get_user_model().objects.get(email__exact=email)
                worker = request.user

                if user.id == worker.id:
                    user = None
                    error_list.append(f"Email: {email} is you're")
                    raise Exception("User overflow")

                user_referer = UserReferer.objects.filter(user__exact=user)

                if user_referer.count():
                    user = None
                    error_list.append(f"{email} has referer")
                    raise Exception("User has referer")
                else:
                    referer = UserReferer()
                    referer.user = user
                    referer.worker = worker
                    referer.save()

            except get_user_model().DoesNotExist:
                error_list.append("User with this email not exists :(")
            except:
                pass
    else:
        form = EmailBinderForm()

    context = {
        "form": form,
        "founded_user": user,
        "error_list": error_list,
    }
    return render(request, "panel/bind_email.html", context)


@login_required(login_url='/accounts/login/')
@permission_required("can_acces_panel")
def bind_promo(request):
    success_msg = None
    promo_codes = None
    if request.method == "POST":
        form = PromoBindingForm(request.POST)
        if form.is_valid():
            form.save(True)
            success_msg = "Promo added succesfully"
    else:
        form = PromoBindingForm()

    try:
        promo_codes = BonusModel.objects.all()
    except:
        pass

    context = {
        "form": form,
        "success_msg": success_msg,
        # "error_list": error_list,
        "promo_codes": promo_codes,
    }
    return render(request, "panel/bind_promo.html", context)


@login_required(login_url='/accounts/login/')
@permission_required("can_acces_panel")
def user(request):
    referals = None

    try:
        referals = UserReferer.objects.filter(worker__exact=request.user)
    except:
        pass

    context = {
        "referals": referals,
    }

    return render(request, "panel/user.html", context)


@login_required(login_url='/accounts/login/')
@permission_required("can_acces_panel")
def user_detail(request, user_id):

    user = get_user_model().objects.get(id=user_id)

    try:
        referal = UserReferer.objects.get(user=user)
        if referal.worker != request.user:
            return redirect(reverse_lazy("panel:user"))
    except:
        return redirect(reverse_lazy("panel:user"))

    context = {
        "user": user,
    }

    return render(request, "panel/user_details.html", context)


@login_required(login_url="/accounts/login/")
@permission_required("can_acces_panel")
def user_messaging(request, user_id):
    user = get_user_model().objects.get(id=user_id)

    try:
        referal = UserReferer.objects.get(user=user)
        if referal.worker != request.user:
            return redirect(reverse_lazy("panel:user"))
    except:
        return redirect(reverse_lazy("panel:user"))

    context = {
        "user": user,
    }

    return render(request, "panel/user_messaging.html", context)

@login_required(login_url='/accounts/login/')
@permission_required("can_acces_panel")
def user_support(request, user_id):
    user = get_user_model().objects.get(id=user_id)

    try:
        referal = UserReferer.objects.get(user=user)
        if referal.worker != request.user:
            return redirect(reverse_lazy("panel:user"))
    except:
        return redirect(reverse_lazy("panel:user"))

    msg_send_form = MessageSendPanelForm()

    context = {
        "user": user,
        "form": msg_send_form,
    }
    return render(request, "panel/user_support.html", context)



@login_required(login_url='/accounts/login/')
@permission_required("can_acces_panel")
@require_http_methods(["POST",])
def send_support_message(request):
    worker = request.user
    
    try:
        user = UserReferer.objects.get(Q(worker_id=worker.id)).user
    except UserReferer.DoesNotExist:
        user = worker
    except UserReferer.MultipleObjectsReturned:
        user = worker
    
    form = MessageSendPanelForm(request.POST)
    if form.is_valid():
        message = form.save(commit=False)
        message.sender = get_user_model().objects.get(id=worker.id)
        message.receiver = get_user_model().objects.get(id=user.id)
        message.save()
    

    return redirect(reverse_lazy("panel:user_support", kwargs={"user_id": user.id}))
        