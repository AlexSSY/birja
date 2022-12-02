from django.urls import path
from . import views

app_name ="main"

urlpatterns = [
    path('', views.index, name="index"),
    path('bonus/<str:bonus_name>', views.bonus, name="bonus"),
]