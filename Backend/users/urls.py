from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('users/register/', views.RegisterUserView.as_view(), name='register'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('addresses/', views.AddressListCreateView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', views.AddressRetrieveUpdateDestroyView.as_view(), name='address-detail'),
    path('stores/', views.StoreListCreateView.as_view(), name='store-list-create'),
    path('stores/<int:pk>/', views.StoreRetrieveUpdateDestroyView.as_view(), name='store-detail'),
    path('jwt/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

