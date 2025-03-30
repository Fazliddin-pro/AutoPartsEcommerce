from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Address, Store

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'avatar', 'role', 'is_verified']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'], 
            phone_number=validated_data['phone_number']
        )
        try:
            validate_password(validated_data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        user.set_password(validated_data['password'])
        user.save()
        return user


class AddressSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Address
        fields = ['id', 'city', 'street', 'house', 'apartment', 'postal_code', 'is_default', 'user']
        read_only_fields = ['user']


class StoreSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Store
        fields = ['id', 'name', 'logo', 'description', 'is_active', 'user']
        read_only_fields = ['user']
