"""
Module containing the `EmailOrUsernameModelBackend` class.
"""

from typing import Optional

from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest

from account.models import User


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Class to authenticate the user using either their username or email.
    """

    def authenticate(self, _request: HttpRequest, username: Optional[str], password: Optional[str]) -> Optional[User]:
        """
        Authenticates the user using either their username or email.
        """
        if not username or not password:
            return None

        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            return None

        if not user.check_password(password):
            return None

        return user
