from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Address, Store

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'avatar', 'role', 'is_verified']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(email=validated_data['email'], phone_number=validated_data['phone_number'])
        user.set_password(validated_data['password'])  # Хэшируем пароль
        user.save()
        return user


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'city', 'street', 'house', 'apartment', 'postal_code', 'is_default', 'user']
        read_only_fields = ['user']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'logo', 'description', 'is_active', 'user']
        read_only_fields = ['user']
