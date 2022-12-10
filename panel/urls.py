from django.urls import path
from . import views

app_name = "panel"

urlpatterns = [
    path("", views.index, name="index"),
    path("bind/", views.bind, name="bind"),
    path("bind/email/", views.bind_email, name="bind_email"),
    path("bind/promo/", views.bind_promo, name="bind_promo"),
]