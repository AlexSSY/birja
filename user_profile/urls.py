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
    path('course', views.get_invest_course, name="course"),
    path('p2p/<int:page_size>/<int:page_number>/<str:fiat>/<str:token>/<str:trade_type>', views.get_p2p_binance, name="get_p2p_binance"),
    path('settings/photo', views.change_user_photo, name='change_user_photo'),
    path('settings/password', views.change_user_password, name='change_user_password'),
    path('getcoins', views.get_coins_amount, name='get_coins_amount')
]