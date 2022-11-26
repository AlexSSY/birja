from django.urls import path
from . import views

urlpatterns = [
    path('get/<int:id>/', views.get_profile),
    path('edit/<int:id>/', views.edit_profile),
]