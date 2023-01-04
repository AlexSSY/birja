from django.urls import path
from . import views

app_name = "user_profile"

urlpatterns = [
    path('wallet', views.wallet, name="wallet"),
    path('deposit', views.deposit, name="deposit"),
    path('withdraw', views.withdraw, name="withdraw"),
    path('transactions', views.transactions, name="transactions"),
    path('transfer', views.transfer, name="transfer"),
    path('invest', views.invest, name="invest"),
    path('affiliate', views.affiliate, name="affiliate"),
    path('api', views.api, name="api"),
    path('settings', views.settings, name="settings"),
    path('verif', views.verif, name="verif"),
    path('register', views.RegisterUser.as_view(), name="register"),
    path('login', views.LoginUser.as_view(), name="login"),
    path('logout', views.custom_logout, name="logout"),
    path('terms', views.terms, name="terms"),
    path('privacy_notice', views.privacy_notice, name="privacy_notice"),
    path('cookies_policy', views.cookies_policy, name="cookies_policy"),
    path('amlkyc_policy', views.amlkyc_policy, name="amlkyc_policy"),
    path('fees', views.fee, name="fees"),
    path('balance', views.get_balance, name="balance"),
]