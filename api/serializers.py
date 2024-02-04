from rest_framework import serializers
from .models import Product
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from .user_serializers import UserPublicSerializer


class UserSerializer2(serializers.Serializer):
    username = serializers.CharField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField(read_only=True)
    # username = serializers.SerializerMethodField(read_only=True)

    # for joins
    user_id = serializers.IntegerField(source='user.id', read_only=True)  # For other models we can use this way
    user_details = UserPublicSerializer(source='user', read_only=True)  # specifically for User model we are creating separate file
    user_details2 = UserSerializer2(source='user', read_only=True)

    class Meta:
        model = Product
        fields = [
            'user_id',
            'user_details',
            'user_details2',
            'title',
            'content',
            'price',
            'sale_price',
            'tag',
            # 'username'
        ]

    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.save()
    #     return product

    # If we want to process the data for each object, then instead of looping through the
    # queryset we can use this method - get_<attribute_name>
    def get_tag(self, obj):
        return 'Premium' if obj.price > 10 else 'Basic'

    # def get_username(self, obj):
    #     return obj.user.username

    # validate_<field_name>
    # These methods must always return the value
    # validate_price and validate will be called on serializer.is_valid()
    def validate_price(self, value):
        print(value, 'value')
        if int(value) < 5:
            raise serializers.ValidationError('Price must be greater or equal to 5')
        return value

    # def validate(self, data):
    #     print('ENTER')
    #     print(data, 'data')
    #     raise serializers.ValidationError({'user_id': "Email address is already in use."})


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User(username=validated_data.get('username'))
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    # def validate_username(self, value):
    #     validator = EmailValidator()
    #     validator(value)
    #     return value


class LoginSerializer(serializers.Serializer):
    # Here serializers.Serializer is used instead of ModelSerializer
    # This is because we dont need a model for this serializer as we just want to validate
    # the request data, and dont want to save any data in the model.

    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)
