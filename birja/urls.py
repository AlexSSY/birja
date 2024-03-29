"""birja URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from user_profile.api_routing import stake_router
from user_profile.admin import worker_admin

urlpatterns = [
    path('', include("main.urls")), 
    path('profile/', include('user_profile.urls')),
    path('support/', include('support.urls')),
    #path('panel/', include('panel.urls')),
    path('admin/', admin.site.urls, name='admin_index'),
    path('panel/', worker_admin.urls, name='panel'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(stake_router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)