from django.urls import path
from . import views

app_name ="main"

urlpatterns = [
    path('', views.index, name="index"),
    path('nft/', views.nft, name="nft"),
    path('trading/<str:symbol_source>/<str:symbol_dest>', views.trading, name="trading"),
    path('bonus/<str:bonus_name>', views.bonus, name="bonus"),
    path('p2p/', views.p2p, name="p2p"),
    path('market/', views.market_tools, name="market_tools"),
    path('market/cap', views.crypto_market_cap, name="market_cap"),
    path('market/screener', views.market_screener, name="market_screener"),
    path('market/technical', views.market_tech, name="market_tech"),
    path('market/cross', views.market_cross, name="market_cross"),
    path('market/heat', views.market_heat, name="market_heat"),
    path('swap', views.swap, name="swap"),
    path('chat', views.chat, name="chat"),
    path('chat_message', views.chat_message, name="chat_message"),
]