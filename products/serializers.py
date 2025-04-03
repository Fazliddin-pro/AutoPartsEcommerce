from rest_framework import serializers
from .models import Product, Category, ProductImage, ProductProperties


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'products_count', 'subcategories']

    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data


class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main']


class ProductPropertiesSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductProperties.objects.create(product_id=product_id, **validated_data)
    
    class Meta:
        model = ProductProperties
        fields = ['id', 'name', 'value']


class ProductSerializer(serializers.ModelSerializer):
    store = serializers.StringRelatedField()
    category = serializers.HyperlinkedRelatedField(
        view_name='category-detail',
        read_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)
    properties = ProductPropertiesSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'stock',
            'last_update', 'images', 'properties', 'store', 'category'
        ]

