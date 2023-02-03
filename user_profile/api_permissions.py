from rest_framework.permissions import BasePermission


class IsAmountEnoughPermission(BasePermission):
    
    def has_permission(self, request, view):
        return True