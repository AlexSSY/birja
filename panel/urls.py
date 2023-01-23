from django.urls import path
from . import views

app_name = "panel"

urlpatterns = [
    path("", views.index, name="index"),
    path("bind/", views.bind, name="bind"),
    path("user/", views.user, name="user"),
    path("user/<int:user_id>", views.user_detail, name="user_details"),
    path("user/<int:user_id>/messaging", views.user_messaging, name="user_messaging"),
    path("user/<int:user_id>/support", views.user_support, name="user_support"),
    path("user/support/send", views.send_support_message, name="send_support_message"),
    path("bind/email/", views.bind_email, name="bind_email"),
    path("bind/promo/", views.bind_promo, name="bind_promo"),
]