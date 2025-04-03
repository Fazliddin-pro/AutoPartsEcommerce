from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('images', views.ProductImageViewSet, basename='product-images')
products_router.register('properties', views.ProductPropertiesViewSet, basename='product-properties')

urlpatterns = router.urls + products_router.urls