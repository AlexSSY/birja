from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User


def get_profile(request, id):
    user = User.objects.get(id=id)
    data = {
        # User data
        "username": user.username,
        "last_name": user.last_name,
        "email": user.email,
        "date_joined": user.date_joined,
        "first_name": user.first_name,
        # User Profile data
        "photo": user.userprofile.photo.path,
        "postal_code": user.userprofile.postal_code,
        "country": user.userprofile.country,
        "city": user.userprofile.city,
        "present_address": user.userprofile.present_address,
        "phone_number": user.userprofile.phone_number,
    }
    return JsonResponse(data)


def edit_profile(request, id):
    pass
