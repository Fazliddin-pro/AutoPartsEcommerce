from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartRetrieveView, CartItemViewSet, OrderViewSet

cart_router = DefaultRouter()
cart_router.register(r'items', CartItemViewSet, basename='cartitem')

main_router = DefaultRouter()
main_router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('carts/detail/', CartRetrieveView.as_view(), name='cart-detail'),
    path('carts/', include(cart_router.urls)),
    path('', include(main_router.urls)),
]
