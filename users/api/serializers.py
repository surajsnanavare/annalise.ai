import uuid
from rest_framework import serializers
from users.models import User


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializers signup requests and creates a new user.
    """

    # Make sure password can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    # Make sure Client should not be able to send token
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'token']


class UserSerializer(serializers.ModelSerializer):
    """
    Handle serialization and deserialization of User objects.
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
