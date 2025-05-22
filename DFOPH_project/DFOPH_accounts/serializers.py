from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import User, Role

#serializers.py – Responsible for validating data and saving it to the database

# Get your custom User model (extending AbstractUser)
UserModel = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
     # Use SlugRelatedField to map role name (slug_field) to Role instance
    role = serializers.SlugRelatedField(
        queryset=Role.objects.all(),
        slug_field='name'  # field in Role model to match (e.g. "buyer", "seller")
    )
    # Fields for entering and confirming password
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm password")

    class Meta:
        model = User  # This tells the serializer which model to use
        fields = ['username', 'email', 'password', 'password2', 'role', 'address',]

    # Validate that both passwords match
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    # Save the new user to the database with hashed password
    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 (we don't need to store it)
        password = validated_data.pop('password')  # Get the password
        user = User(**validated_data)  # Create a user instance without saving
        user.set_password(password)  # Hash the password before saving!
        user.save()  # Save to database
        return user

# Create a custom authentication backend class that inherits from Django's ModelBackend
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email:
            raise serializers.ValidationError({'email': 'Email is required'})
        if not password:
            raise serializers.ValidationError({'password': 'Password is required'})

        # Authenticate using email instead of username
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError({'detail': 'Invalid email or password'})

        # Pass username and password to the parent to generate tokens
        data = super().validate(attrs)

        # Optionally add extra user info to response
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'role': user.role.name, 
        }

        return data