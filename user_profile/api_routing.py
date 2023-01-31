from rest_framework.routers import SimpleRouter, DefaultRouter
from .api_views import StakeModelAPIView


stake_router = DefaultRouter()
stake_router.register(r'stake', StakeModelAPIView)