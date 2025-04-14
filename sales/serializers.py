from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from products.serializers import ProductSerializer
from users.serializers import UserSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']
        read_only_fields = ['id', 'product']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']
        read_only_fields = ['id', 'user', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price_at_purchase']
        read_only_fields = ['id', 'price_at_purchase']
    
    def create(self, validated_data):
        product = validated_data['product']
        validated_data['price_at_purchase'] = product.price
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    items = OrderItemSerializer(many=True, write_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'created_at', 'updated_at',
            'status', 'total_price',
            'shipping_address', 'billing_address',
            'payment_status', 'order_items', 'items'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'total_price', 'order_items']
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one order item must be provided.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        user = self.context.get('request').user
        order = Order.objects.create(user=user, status='pending', total_price=0, **validated_data)
        
        total = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data.get('quantity', 1)
            price = product.price
            total += price * quantity
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_purchase=price
            )
        order.total_price = total
        order.save()
        return order
