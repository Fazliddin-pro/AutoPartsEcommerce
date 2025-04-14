from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartRetrieveView, CartItemViewSet

router = DefaultRouter()
router.register(r'items', CartItemViewSet, basename='cartitem')

urlpatterns = [
    path('carts/', CartRetrieveView.as_view(), name='cart-detail'),
    path('carts/', include(router.urls)),
]
