from rest_framework import generics, permissions
from .permissions import IsOwner
from .models import CustomUser, Address, Store
from .serializers import (
    AddressSerializer,
    StoreSerializer,
    UserSerializer,
    RegisterSerializer,
)


class RegisterUserView(generics.CreateAPIView):
    """Handles user registration."""
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class UserListView(generics.ListAPIView):
    """Retrieves a list of all users (admin only)."""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Retrieves and updates the authenticated user's profile."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class AddressListCreateView(generics.ListCreateAPIView):
    """Retrieves a list of user addresses and allows users to create new addresses"""
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user).select_related('user')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user_id': self.request.user.id})
        return context


class AddressRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates, and deletes a user address."""
    serializer_class = AddressSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user).select_related('user')


class StoreListCreateView(generics.ListCreateAPIView):
    """Retrieves a list of stores and allows sellers to create new stores."""
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Store.objects.filter(user=self.request.user).select_related('user')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user_id': self.request.user.id})
        return context


class StoreRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates, and deletes a store."""
    serializer_class = StoreSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Store.objects.filter(user=self.request.user).select_related('user')
