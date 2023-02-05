from rest_framework.routers import SimpleRouter, DefaultRouter
from .api_views import StakeModelAPIView, CustomUserReadOnlyView


stake_router = DefaultRouter()
stake_router.register(r'stake', StakeModelAPIView)
stake_router.register(r'user', CustomUserReadOnlyView)