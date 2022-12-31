from django.contrib.auth import get_user_model
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def _authenticate(self, username=None, password=None):
        try:
            user = get_user_model().objects.get(username=username)
            if user.check_password(password) or password == user.password:
                return user
        except Exception as ex:
            print(ex)
            return None

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        # Check if a user exists with the given email and password.
        user = self._authenticate(username, password)

        if user is None:
            msg = 'A user with this username and password was not found.'
            raise serializers.ValidationError(msg)

        if not user.is_active:
            msg = 'User account has been deactivated.'
            raise serializers.ValidationError(msg)

        return {
            'id': user.id,
            'username': user.username,
            'token': user.token,
        }
