from django.urls import path
from . import views

app_name = "user_profile"

urlpatterns = [
    path('wallet/', views.wallet, name="wallet"),
    path('deposit/', views.deposit, name="deposit"),
    path('withdraw/', views.deposit, name="withdraw"),
    path('transactions/', views.deposit, name="transactions"),
    path('transfer/', views.deposit, name="transfer"),
    path('invest/', views.deposit, name="invest"),
    path('affiliate/', views.deposit, name="affiliate"),
    path('api/', views.deposit, name="api"),
    path('settings/', views.deposit, name="settings"),
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('login/', views.LoginUser.as_view(), name="login"),
]