from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from .models import Cart, CartItem, Order
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer

class CartRetrieveView(generics.RetrieveAPIView):
    """
    Retrieves the cart for the authenticated user.
    If a cart does not exist, it is created.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class CartItemViewSet(viewsets.ModelViewSet):
    """
    API for adding, changing and deleting products into carts.
    """
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing orders.
    Users can list, retrieve, create, update, and delete their orders.
    Only orders belonging to the authenticated user are returned.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context