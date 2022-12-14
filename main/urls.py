from django.urls import path
from . import views

app_name ="main"

urlpatterns = [
    path('', views.index, name="index"),
    path('trading/<str:symbol_source>/<str:symbol_dest>', views.trading, name="trading"),
    path('bonus/<str:bonus_name>', views.bonus, name="bonus"),
    path('p2p/', views.p2p, name="p2p"),
]