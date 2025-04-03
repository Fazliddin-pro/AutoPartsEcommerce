from rest_framework import permissions

from users.models import Store
from .models import Product, ProductImage, ProductProperties


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    Read-only permissions are allowed for any request.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_staff
        )

class IsOwnerOrAdminOrSuperuser(permissions.BasePermission):
    """
    Custom permission to allow:
    - Owners of the store to add/edit their products, images, and properties.
    - Users with role 'admin' to add/edit products, images, and properties.
    - Superusers (admins) to add/edit products, images, and properties.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            if not request.user.is_authenticated:
                return False
            
            if request.user.is_staff:
                return True
            
            store_pk = view.kwargs.get('store_pk')
            if store_pk:
                try:
                    store = Store.objects.get(pk=store_pk)
                    if store.owner == request.user or request.user.role == 'admin':
                        return True
                except Store.DoesNotExist:
                    return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True
        
        if isinstance(obj, Product):
            if obj.store.owner == request.user or request.user.role == 'admin':
                return True
        if isinstance(obj, ProductImage) or isinstance(obj, ProductProperties):
            if obj.product.store.owner == request.user or request.user.role == 'admin':
                return True

        return False
