from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# Retrieves the custom User model defined in your app (users.models.User)
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer used to expose user profile information via API endpoints 
    (e.g., /api/user/profile/). Excludes sensitive data like password hash.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'plan', 'role', 'daily_quota_used', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer specifically for registering a new user. 
    It handles password validation and confirmation fields.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
    
    def validate(self, attrs):
        """
        Custom validation to ensure the two password fields match.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs
    
    def create(self, validated_data):
        """
        Creates a new user instance using the secure create_user method.
        """
        validated_data.pop('password2')  # Remove the confirmation field as it is not part of the model
        # Use the manager's create_user method to ensure the password is hashed correctly
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user