from django.urls import path
from . import views

app_name = "support"

urlpatterns = [
     path("", views.lobby, name="lobby"),
     path("send", views.send_message, name="send"),
     path("jsend", views.send_message_json, name="send_json"),
     path("list", views.get_message_list_user, name="list_user"),
     path("list/<int:user_id>", views.get_message_list, name="list"),
]