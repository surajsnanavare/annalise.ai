import jwt
from datetime import datetime, timedelta
from core.models import BaseModel
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser, BaseModel):
    """
    Extended user model with additional fields.
    """
    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )

    first_name = models.CharField("first name", max_length=150, null=False)
    last_name = models.CharField("last name", max_length=150, null=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Creates a JSON Web Token with the user's ID and an expiry
        date set to 60 days in the future.
        """

        dt = datetime.now() + timedelta(days=settings.TOKEN_EXPIRY_DAYS)

        return jwt.encode({
            'id': str(self.pk),
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
