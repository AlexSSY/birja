from django.urls import path
from . import views

app_name = "support"

urlpatterns = [
     path("", views.lobby, name="lobby"),
     path("send/", views.send_message, name="send"),
     path("list/", views.get_message_list, name="list"),
]