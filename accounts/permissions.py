from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class IsBayAdmin(BasePermission):
    """
    Allows access only to delivery admin users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.role == 'bay_admin') 
        else:
            raise AuthenticationFailed(detail="Authentication credentials were not provided")
        
class IsShippingAdmin(BasePermission):
    """
    Allows access only to delivery admin users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.role == 'shipping_admin')
        else:
            raise AuthenticationFailed(detail="Authentication credentials were not provided")
        
        
class IsShippingAdminOrBayAdmin(BasePermission):
    """
    Allows access only to delivery admin users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.role == 'bay_admin') or bool(request.user and request.user.role == 'shipping_admin')
        else:
            raise AuthenticationFailed(detail="Authentication credentials were not provided")
        
        
class IsAdminOrShippingAdmin(BasePermission):
    """
    Allows access only to delivery admin users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.role == 'admin') or bool(request.user and request.user.role == 'shipping_admin')
        else:
            raise AuthenticationFailed(detail="Authentication credentials were not provided")
        
        
class IsAdminorReadOnly(BasePermission):
    """
    Allows access only to delivery admin users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.method in SAFE_METHODS) or bool(request.user and request.user.role == 'admin') or bool(request.user and request.user.role == 'shipping_admin') or bool(request.user and request.user.role == 'bay_admin')
        else:
            raise AuthenticationFailed(detail="Authentication credentials were not provided")