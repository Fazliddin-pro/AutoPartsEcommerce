from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import CustomUser, Address, Store
from .serializers import AddressSerializer, StoreSerializer, UserSerializer, RegisterSerializer

class RegisterUserView(generics.CreateAPIView):
    """Handles user registration."""
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class UserListView(generics.ListAPIView):
    """Retrieves a list of all users."""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Retrieves and updates the authenticated user's profile."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class AddressListCreateView(generics.ListCreateAPIView):
    """Retrieves a list of user addresses and creates a new address."""
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Теперь user добавляется через контроллер


class AddressRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates, and deletes a user address."""
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class StoreListCreateView(generics.ListCreateAPIView):
    """Retrieves a list of stores and allows sellers to create new stores."""
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Store.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.role != 'seller':
            raise PermissionDenied('Only sellers can create a store.')
        serializer.save(user=self.request.user)


class StoreRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates, and deletes a store."""
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Store.objects.filter(user=self.request.user)
