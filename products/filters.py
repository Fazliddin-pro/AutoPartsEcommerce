from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'category_id': ['exact'],
            'store_id': ['exact'],
            'price': ['gt', 'lt'],
        }
