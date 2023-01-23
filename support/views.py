from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.humanize.templatetags.humanize import naturaltime

from .forms import MessageSendForm
from .models import SupportMessage
from user_profile.models import UserReferer


@login_required
def lobby(request):
    worker = None
    try:
        worker = UserReferer.objects.filter(worker_id__iexact=request.user.id)
    except Exception as e:
        pass

    worker_id = worker.id if worker else 0

    form = MessageSendForm(initial={
        "sender": request.user.id,
        "receiver": worker_id,
    })

    context = {
        'form': form,
    }
    return render(request, "support/lobby.html", context)


@require_http_methods(["POST", ])
def send_message(request):

    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "Not authenticated",
        })

    current_user = request.user
    worker = None

    try:
        user_referer = UserReferer.objects.get(user=current_user)
        worker = user_referer.worker
    except Exception as e:
        pass

    form = MessageSendForm(request.POST)

    if form.is_valid():
        message = form.save(commit=False)
        message.sender = get_user_model().objects.get(id=current_user.id)
        message.receiver = worker if worker else get_user_model().objects.get(id=1)
        message.save()

    data = {
        "user": current_user.email,
        "worker": worker.email,
    }
    # return JsonResponse(data)
    return redirect(reverse_lazy("support:lobby"))


@login_required
def get_message_list(request, user_id):
    result = None
    user = get_user_model().objects.filter(id=user_id).first()

    if user is None:
        return HttpResponseBadRequest("user not found")
    elif UserReferer.objects.filter(Q(worker=request.user.id) & Q(user=user)).first() is None:
        return HttpResponseBadRequest("user is not your referal")

    try:
        result = SupportMessage.objects.filter(Q(sender_id=user.id) | Q(receiver_id=user.id)).order_by("time")
    except:
        pass

    data = {
        "messages": []
    }

    for msg in result:
        type = "recv"

        if msg.sender.id == request.user.id:
            type = "send"

        data["messages"].append(
            {
                "time": naturaltime(msg.time),
                "message": msg.message,
                "type": type,
            }
        )

    return JsonResponse(data)
