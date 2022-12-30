import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


def _authenticate_credentials(self, token):
    """
    Method to autheticate user using provided JWT token
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY,
            algorithms='HS256'
        )
    except BaseException:
        msg = 'Authentication failed! Bad token.'
        raise exceptions.AuthenticationFailed(msg)

    try:
        user = User.objects.get(pk=payload['id'])
    except User.DoesNotExist:
        msg = 'Authentication failed! User account does not exist!.'
        raise exceptions.AuthenticationFailed(msg)

    if not user.is_active:
        msg = 'Authentication failed! User account has been deactivated.'
        raise exceptions.AuthenticationFailed(msg)

    return (user, token)


class JWTAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class for JWT authentication.
    """
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1 or len(auth_header) > 2:
            msg = 'Authentication failed! Incomplete token.'
            raise exceptions.AuthenticationFailed(msg)

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix != auth_header_prefix:
            msg = 'Authentication failed! Wrong prefix.'
            raise exceptions.AuthenticationFailed(msg)

        return _authenticate_credentials(request, token)
