from rest_framework import generics, viewsets, permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Category, ProductImage, ProductProperties
from .serializers import ProductSerializer, CategorySerializer, ProductImageSerializer, ProductPropertiesSerializer
from .permissions import IsAdminOrReadOnly
from .filters import ProductFilter
from .pagination import DefaultPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.annotate(products_count=Count('products'))
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(category_id=kwargs['pk']).exists():
            return Response({'error': 'Category cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)
 

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category', 'store').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}
    
    def perform_create(self, serializer):
        serializer.save(store=self.request.user.store)


class ProductImageViewSet(viewsets.ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class ProductPropertiesViewSet(viewsets.ModelViewSet):
    serializer_class = ProductPropertiesSerializer

    def get_queryset(self):
        return ProductProperties.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

